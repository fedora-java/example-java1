#!/bin/bash
set -e

if ! [ -f "$1" -a -n "$2" ]; then
    echo "Usage: build-all.sh mock-config.cfg common-collection-name" 1>&2
    exit 2
fi

packages="example-java1 maven-foo maven-bar ivy-baz ivy-publish"

rm -rf srpms/ meta-repo/ collection-repo/ result/
mkdir srpms meta-repo collection-repo
for pkg in $packages; do
    rpmbuild -bs -D"_sourcedir $pkg" -D"_srcrpmdir srpms" $pkg/*.spec
    [ $pkg == example-java1 ] || srpm_list="$srpm_list `echo srpms/$pkg-*.src.rpm`"
done

python << EOF
config_opts = {}
with open("$1") as f:
    code = compile(f.read(), "$1", 'exec')
exec(code)
config_opts['chroot_setup_cmd'] = "install @build scl-utils-build $2-scldevel"
config_opts['root'] = 'example-java1-meta'
with open("tmp-config-meta.cfg", 'w') as br_dest:
    for k, v in list(config_opts.items()):
        br_dest.write("config_opts[%r] = %r\n" % (k, v))
config_opts['yum.conf'] += "\n[meta]\nbaseurl=file://$PWD/meta-repo"
config_opts['chroot_setup_cmd'] = "install @build example-java1-build"
config_opts['root'] = 'example-java1-collection'
with open("tmp-config-collection.cfg", 'w') as br_dest:
    for k, v in list(config_opts.items()):
        br_dest.write("config_opts[%r] = %r\n" % (k, v))
EOF

mock -r tmp-config-meta.cfg srpms/example-java1-*.src.rpm --resultdir=result
mv result/example-java1-*.rpm meta-repo/
(cd meta-repo && createrepo_c .)
mockchain -r tmp-config-collection.cfg ${srpm_list}
