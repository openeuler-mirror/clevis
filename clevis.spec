Name:          clevis
Version:       11
Release:       5
Summary:       A plugable framework for automated decryption

License:       GPLv3+
URL:           https://github.com/latchset/%{name}
Source0:       https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz

Patch1:        backport-Delete-remaining-references-to-the-removed-http-pin.patch
Patch2:        backport-Install-cryptsetup-and-tpm2_pcrlist-in-the-initramfs.patch
Patch3:        backport-Add-device-TCTI-library-to-the-initramfs.patch

BuildRequires: meson cmake jansson jose pkgconfig libjose-devel gdb asciidoc gcc openssl-devel
BuildRequires: desktop-file-utils libudisks2-devel audit-libs-devel tang dracut pkgconfig
BuildRequires: bash-completion tpm2-tools luksmeta libluksmeta-devel ninja-build systemd curl
Requires:      tpm2-tools jose curl coreutils cryptsetup luksmeta
Provides:      clevis-luks
Obsoletes:     clevis-luks

%description
Clevis is a plugable framework for automated decryption. It can be used 
to provide automated decryption of data or even automated unlocking of 
LUKS volumes.

This package allows users to bind a LUKS volume using a pin so that it can
be automatically unlocked. Upon successful completion of binding, the disk
can be unlocked using one of the provided unlockers.

%package systemd
Summary:       Systemd integration for clevis
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      systemd nc

%description systemd
The systemd unlocker attempts to automatically unlock LUKSv1 _netdev block devices from /etc/crypttab.

%package dracut
Summary:       Dracut integration for clevis
Requires:      %{name}-systemd%{?_isa} = %{version}-%{release}
Requires:      dracut-network

%description dracut
The dracut unlocker attempts to automatically unlock volumes during early boot. 

%package udisks2
Summary:       Udisks2 integration for clevis
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description udisks2
The udisks2 unlocker attempts to automatically unlock volumes in desktop environments 
that use UDisks2 or storaged (like GNOME). 

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
%meson -Duser=clevis -Dgroup=clevis
%meson_build

%install
%meson_install

%check
# add test for clevis-luks-udisks2.desktop: validates the clevis-luks-udisks2.desktop 
# and prints warnings/errors about desktop entry specification violations
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-luks-udisks2.desktop
%meson_test

%files
%defattr(-,root,root)
%license COPYING*
%{_datadir}/bash-completion/
%{_bindir}/clevis
%{_bindir}/clevis-decrypt*
%{_bindir}/clevis-encrypt*
%{_bindir}/%{name}-luks*

%files systemd
%defattr(-,root,root)
%{_unitdir}/clevis-luks-askpass*
%{_libexecdir}/clevis-luks-askpass

%files dracut
%defattr(-,root,root)
%{_prefix}/lib/dracut/modules.d/60clevis/*

%files udisks2
%defattr(-,root,root)
%{_sysconfdir}/xdg/autostart/clevis-luks-udisks2.desktop
%attr(4755, root, root) %{_libexecdir}/clevis-luks-udisks2

%files help
%defattr(-,root,root)
%{_mandir}/man*

%changelog
* Sat Dec 12 2020 Liquor <lirui130@huawei.com> - 11-5
- Delete remaining references to the removed http pin
  Install cryptsetup and tpm2_pcrlist in the initramfs
  Add device TCTI library to the initramfs

* Mon May 25 2020 openEuler Buildteam <buildteam@openeuler.org> - 11-4
- Rebuild for clevis

* Fri Oct 18 2019 openEuler Buildteam <buildteam@openeuler.org> - 11-3
- Add COPYING.openssl

* Wed Sep 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 11-2
- Adjust requires

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 11-1
- Package init

