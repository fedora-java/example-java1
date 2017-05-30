#!/bin/bash
set -e

if ! [ -f "$1" -a -n "$2" ]; then
    echo "Usage: build-all.sh mock-config.cfg common-collection-name" 1>&2
    exit 2
fi

packages="example-java1 maven-foo maven-bar ivy-baz ivy-publish"

rm -rf work
mkdir -p work/{srpms,repodata}
for pkg in $packages; do
    rpmbuild -bs -D"_sourcedir $pkg" -D"_srcrpmdir work/srpms" $pkg/*.spec
    [ $pkg == example-java1 ] || srpm_list="$srpm_list `echo work/srpms/$pkg-*.src.rpm`"
done

python << EOF
config_opts = {}
with open("$1") as f:
    code = compile(f.read(), "$1", 'exec')
exec(code)
config_opts['chroot_setup_cmd'] = "install @build scl-utils-build $2-scldevel"
config_opts['root'] = 'example-java1-meta'
with open("work/tmp-config-meta.cfg", 'w') as br_dest:
    for k, v in list(config_opts.items()):
        br_dest.write("config_opts[%r] = %r\n" % (k, v))
config_opts['chroot_setup_cmd'] = "install @build example-java1-build"
config_opts['root'] = 'example-java1-collection'
with open("work/tmp-config-collection.cfg", 'w') as br_dest:
    for k, v in list(config_opts.items()):
        br_dest.write("config_opts[%r] = %r\n" % (k, v))
EOF

mock -r work/tmp-config-meta.cfg work/srpms/example-java1-*.src.rpm --resultdir=work/
mkdir -p work/results/tmp-config-collection/
mv work/example-java1-*.rpm work/results/tmp-config-collection/
(cd work/results/tmp-config-collection && createrepo_c .)
mockchain -r work/tmp-config-collection.cfg -l work ${srpm_list}
