#!/usr/bin/env sh

# FORMAT:
# local/path   source_url   dest_url
#
# repos are cloned from source_url into folder <local/path>
#   local/path must not contain spaces because i dont want to deal with that.
#   If the folder doesn't exist, its a clone
#   If the folder exists, its an incremental pull
#
# after that, push the repo to dest_url.
#   If there's an error (like source overwrote history with --force) then this
#   doesn't happen. Resolve errors manually.

repos='linux         https://github.com/torvalds/linux.git       git@192.168.69.69:mirrors/linux.git
faithanalog/rtmouse  https://github.com/faithanalog/rtmouse.git  git@192.168.69.69:mirrors/faithanalog-rtmouse.git
xf86-video-amdgpu    https://gitlab.freedesktop.org/xorg/driver/xf86-video-amdgpu.git  git@192.168.69.69:mirrors/xf86-video-amdgpu.git
'

printf '%s' "$repos" | while IFS=' ' read -r path source_url dest_url; do
    # work in repos subdir so we can easily gitignore it
    path="./repos/$path"

    # make parent dir of repo
    mkdir -p "$(dirname "$path")"

    # clone if it doesnt exist already
    if ! [ -d "$path" ]; then
        echo "cloning $source_url into $path"
        git clone --mirror "$source_url" "$path"
    fi

    (
        # enter repo
        cd "$path"
        
        # update all branches from source
        # docs for `git fetch -t` say it fetches tags in addition to a normal
        # fetch. in our testing this was not fully the case, and `git fetch -t`
        # did not fetch new branches.
        echo "pulling updates from $source_url"
        git fetch "$source_url"
        git fetch -t "$source_url"

        # push branches to dest
        echo "pushing updates to $dest_url"
        git push --all "$dest_url"
        git push --tags "$dest_url"
    )
done