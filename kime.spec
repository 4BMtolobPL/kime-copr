Name: kime
Version: 3.2.0
Release: 1%{?dist}
License: GPLv3
Summary: Korean IME
Url: https://github.com/Riey/kime
Source0: %{url}/archive/refs/tags/v%{version}.tar.gz

# NOTE: Currently(3.0.2^git_673_33603e0) `kime.desktop` relies on `kime-xdg-autostart` to be in `/usr/bin` which is same as %%{_bindir} for now. However, restructuring is needed if this changes in the future. Write custom `kime.desktop` independent of source repository.

# hopefully noarch; not tested.

# from README.md of kime github repository,
# build dependencies(package name):
#     meson(meson)
#     ninja(ninja-build)
#     libclang(clang-devel)
#     cargo(cargo)
#     pkg-config(pkgconf-pkg-config)
# optional build dependencies:
#     gtk3(gtk3-devel)
#     gtk4(gtk4-devel)
#     qtbase5-private(qt5-qtbase-private-devel)
#     qtbase6-private(qt6-qtbase-private-devel)
#     libdbus(dbus-devel)
#     xcb(libxcb-devel)
#     fontconfig(fontconfig-devel)
#     freetype(freetype-devel)
#     libxkbcommon(libxkbcommon-devel)
# BuildRequires: cmake
BuildRequires: meson
BuildRequires: ninja-build
BuildRequires: clang-devel
BuildRequires: cargo
BuildRequires: rust
BuildRequires: pkgconf-pkg-config
BuildRequires: gtk3-devel
BuildRequires: gtk4-devel
BuildRequires: qt5-qtbase-private-devel
BuildRequires: qt6-qtbase-private-devel
BuildRequires: dbus-devel
BuildRequires: libxcb-devel
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: libxkbcommon-devel

# check dbus, fontconfig, freetype, libxcb in the future.
# optional runtime dependencies
# gtk3
# gtk4
# qt5
# qt6
# libdbus (dbus-libs) (indicator)
# xcb (candidate)
# fontconfig (xim)
# freetype (xim)
# libxkbcommon (wayland)
Requires: (google-noto-sans-cjk-vf-fonts or google-noto-sans-cjk-fonts)
Requires: im-chooser

Conflicts: kime-git

%description

kime is a fast, lightweight, reliable and highly customizable input engine for Korean input.

%prep
%autosetup

%build
# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- --default-toolchain 1.81.0 --profile default -y
# . "$HOME/.cargo/env"
# export RUSTUP_TOOLCHAIN=1.81.0

# cherry picked from build.sh. will write custom build script if something breaks catastrophically.
# scripts/build.sh -ar

%meson
%meson_build

%check
%meson_test

%install
%meson_install

# Remove the documents copied during the Meson build process so that RPM can manage them
rm -rf %{buildroot}%{_datadir}/doc/kime

# Custom im-chooser compatibility
install -d %{buildroot}%{_sysconfdir}/X11/xinit/xinput.d
cat > %{buildroot}%{_sysconfdir}/X11/xinit/xinput.d/kime.conf << EOF
SHORT_DESC="kime"
XIM=kime
XIM_PROGRAM=%{_bindir}/kime-xim
GTK_IM_MODULE=kime
QT_IM_MODULE=kime
AUXILIARY_PROGRAM=%{_bindir}/kime-indicator
EOF

%files
# Install cargo-built binaries
%{_bindir}/kime
%{_bindir}/kime-check
%{_bindir}/kime-indicator
%{_bindir}/kime-candidate-window
%{_bindir}/kime-xim
%{_bindir}/kime-wayland

# Install engine shared library
%{_libdir}/libkime_engine.so

# Install headers
%{_includedir}/kime_engine.h
%{_includedir}/kime_engine.hpp

# Install desktop file
%{_datadir}/applications/kime.desktop
%{_sysconfdir}/xdg/autostart/kime.desktop

# Install autostart helper script
%{_bindir}/kime-xdg-autostart

# Install icons
%{_datadir}/icons/hicolor/64x64/apps/kime-hangul-black.png
%{_datadir}/icons/hicolor/64x64/apps/kime-hangul-white.png
%{_datadir}/icons/hicolor/64x64/apps/kime-latin-black.png
%{_datadir}/icons/hicolor/64x64/apps/kime-latin-white.png

# Install docs
%doc res/default_config.yaml
%doc docs/CHANGELOG.md
%license LICENSE
%doc NOTICE.md
%doc README.md
%doc README.ko.md

%doc docs/CONFIGURATION.md
%doc docs/CONFIGURATION.ko.md

# Conditional frontend builds
%{_libdir}/gtk-3.0/3.0.0/immodules/libim-kime.so
%{_libdir}/gtk-4.0/4.0.0/immodules/libkime-gtk4.so
%{_libdir}/qt5/plugins/platforminputcontexts/libkimeplatforminputcontextplugin.so
%{_libdir}/qt6/plugins/platforminputcontexts/libkimeplatforminputcontextplugin.so

# Custom im-chooser compatibility
%{_sysconfdir}/X11/xinit/xinput.d/kime.conf

%changelog
* Tue Jul 21 2026 Talmo Kim <108853516+4BMtolobPL@users.noreply.github.com> - 3.2.0-1
- Bump kime version to 3.2.0
- Update kime.spec