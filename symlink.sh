#!/bin/sh

remove() {
	rm -rf ~/.config/hypr
	rm -rf ~/.config/kitty
	rm -rf ~/.config/mypymodules
	rm -rf ~/.config/waybar
	rm -rf ~/.config/wofi
}

symlink() {
    ln -s  ~/.arch-dotfiles/hypr ~/.config/hypr
	ln -s  ~/.arch-dotfiles/kitty ~/.config/kitty
	ln -s  ~/.arch-dotfiles/mypymodules ~/.config/mypymodules
	ln -s  ~/.arch-dotfiles/waybar ~/.config/waybar
	ln -s  ~/.arch-dotfiles/wofi ~/.config/wofi
}

echo "Removing folders"
remove
if ! [[ $1 == 'remove' ]]; then
    echo "Symlinking folders"
	symlink
fi
