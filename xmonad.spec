%global pkg_name xmonad

%global common_summary A tiling window manager

%global common_description xmonad is a tiling window manager for X. Windows are arranged\
automatically to tile the screen without gaps or overlap, maximising\
screen use. All features of the window manager are accessible from\
the keyboard: a mouse is strictly optional. xmonad is written and\
extensible in Haskell. Custom layout algorithms, and other\
extensions, may be written by the user in config files. Layouts are\
applied dynamically, and different layouts may be used on each\
workspace. Xinerama is fully supported, allowing windows to be tiled\
on several screens.

%global ghc_pkg_deps ghc-mtl-devel, ghc-X11-devel

# debuginfo is not useful for ghc
%global debug_package %{nil}

Name:           %{pkg_name}
Version:        0.9.2
Release:        3%{?dist}
Summary:        A tiling window manager

Group:          User Interface/X
License:        BSD
URL:            http://hackage.haskell.org/package/%{name}
Source0:        http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:        xmonad-session.desktop
Source2:        xmonad-start
Source3:        xmonad.desktop
Source4:        README.fedora
Patch1:         xmonad-dynamic-link.patch
# fedora ghc archs:
ExclusiveArch:  %{ix86} x86_64 ppc alpha sparcv9
BuildRequires:  ghc, ghc-doc, ghc-prof
BuildRequires:  ghc-rpm-macros >= 0.7.3
BuildRequires:  hscolour
%{?ghc_pkg_deps:BuildRequires:  %{ghc_pkg_deps}, %(echo %{ghc_pkg_deps} | sed -e "s/\(ghc-[^, ]\+\)-devel/\1-doc,\1-prof/g")}
Requires:       ghc-%{name}-devel = %{version}-%{release}
# required until there is a command to open a system-default xterminal
Requires:       xterm
# for xmessage
Requires:       xorg-x11-apps

%description
%{common_description}


%prep
%setup -q
%patch1 -p1 -b .orig
cp -p %SOURCE4 .


%build
%ghc_lib_build


%install
%ghc_lib_install

install -p -m 0644 -D man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -p -m 0644 -D %SOURCE1 %{buildroot}%{_datadir}/xsessions/%{name}.desktop
install -p -m 0755 -D %SOURCE2 %{buildroot}%{_bindir}/%{name}-start
install -p -m 0644 -D %SOURCE3 %{buildroot}%{_datadir}/applications/%{name}.desktop

rm %{buildroot}%{_datadir}/%{name}-%{version}/man/xmonad.hs


%files
%defattr(-,root,root,-)
%doc CONFIG LICENSE README man/%{name}.hs README.fedora
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-start
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/xsessions/%{name}.desktop


%ghc_binlib_package


%changelog
* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.9.2-3
- Enable build on sparcv9

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.9.2-1
- Update to 0.9.2

* Sat Jan 15 2011 Ben Boeckel <mathstuf@gmail.com> - 0.9.1-12
- Update to cabal2spec-0.22.4
- Rebuild
- Use %%{buildroot}

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-11
- rebuild

* Fri Nov 26 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-10
- backport exceptions changes from upstream darcs for ghc7 base4
- update url and drop -o obsoletes

* Sun Nov 07 2010 Ben Boeckel <mathstuf@gmail.com> - 0.9.1-9
- Rebuild

* Wed Sep 29 2010 jkeating - 0.9.1-8
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-7
- xmonad-start should run xterm in background
- improve README.fedora more

* Sun Sep 12 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-6
- add application desktop file for gnome-session to find xmonad
  so setting /desktop/gnome/session/required_components/windowmanager now works
- add xmonad-dynamic-link.patch to dynamically link customized xmonad
- move display of manpage for new users from xmonad.hs to xmonad-start
  and only display it when no ~/.xmonad/
- drop skel file and dont create ~/.xmonad by default

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-5
- update to ghc-rpm-macros-0.8.1, hscolour and drop doc pkg (cabal2spec-0.22.2)

* Fri Jun 25 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-4
- strip dynamic files (cabal2spec-0.21.4)

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-3
- rebuild against ghc-6.12.2

* Wed Jan 13 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-2
- rebuild against ghc-mtl package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-1
- update to 0.9.1
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common_summary and common_description
- use ghc_name, ghc_binlib_package and ghc_pkg_deps
- build shared library
- drop X11_minver for now: it breaks macros
- drop redundant buildroot and its install cleaning

* Tue Dec  8 2009 Jens Petersen <petersen@redhat.com> - 0.9-4
- drop the ppc build cabal workaround

* Tue Nov 17 2009 Jens Petersen <petersen@redhat.com> - 0.9-3
- use %%ghc_pkg_ver for requires

* Sun Nov 15 2009 Jens Petersen <petersen@redhat.com> - 0.9-2
- also buildrequires and requires ghc-X11-doc

* Sun Nov 15 2009 Jens Petersen <petersen@redhat.com> - 0.9-1
- update to 0.9 (requires ghc-X11 >= 1.4.6.1)
- drop superfluous X11_version from ghc-X11 requires
- rename X11_version to X11_minver
- remove extra xmonad.hs under datadir

* Thu Jul 30 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-15
- rebuild against newer packages from the mass rebuild

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 16 2009 Jens Petersen <petersen@redhat.com> - 0.8.1-13
- buildrequires ghc-rpm-macros (cabal2spec-0.16)
- rebuild for ghc-6.10.3

* Wed May  6 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-12
- applies changes from jens' patch
- renames xmonad.desktop entry
- adds .orig of the xmonad default config
- modifies manpage patch to use 'better' filenames
- renames manpage patch

* Mon Apr 27 2009 Yaakov M. Nemoy <yankee@localhost.localdomain> - 0.8.1-11
- adds runghc hack taken from haddock

* Mon Apr 27 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-10
- converts the sample config into a patch on the upstream source
- renumbers down the source lines

* Mon Apr 20 2009 Jens Petersen <petersen@redhat.com> - 0.8.1-9
- update to latest macros.ghc without ghc_version (cabal2spec-0.15)
- require xorg-x11-apps for xmessage

* Mon Apr  6 2009 Jens Petersen <petersen@redhat.com>
- merge xmonad-session into xmonad-start
- fix with_prof configure test

* Thu Apr 02 2009 Till Maas <opensource@till.name> - 0.8.1-8
- remove tabs in spec
- rename start-xmonad to xmonad-start for consistency with xmonad-session
- add directory creation and exec of xmonad to start-xmonad
- install xmonad.hs that only displays manpage in /etc/skel/.xmonad/xmonad.hs
- add xterm dependency

* Tue Mar 31 2009 Yaakov M. Nemoy <yankee@localhost.localdomain> - 0.8.1-7
- added session and start scripts

* Mon Mar 30 2009 Till Maas <opensource@till.name> - 0.8.1-6
- add desktop file
- install man page
- include sample config file (xmonad.hs)
- include other documentation files

* Tue Mar 17 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-5
- refixes permissions after doing it wrong the first time

* Fri Mar 13 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-4
- fixed license to BSD
- fixed version of X11 to be a tad more flexible
- fixes permissions of /usr/bin/xmonad

* Mon Mar  2 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-3
- updated to newest cabal2spec 0.12
- this includes the shiny new devel package

* Tue Feb 24 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.8.1-2
- updated spec to meet new guidelines ala cabal2spec 0.7

* Wed Jan 21 2009 ynemoy <ynemoy@fedoraproject.org> - 0.8.1-1
- initial packaging for Fedora created by cabal2spec
