%global X11_version 1.4.3

%bcond_without doc
%bcond_without prof

# ghc does not emit debug information
%global debug_package %{nil}

Name:           xmonad
Version:        0.8.1
Release:        13%{?dist}
Summary:        A tiling window manager

Group:          User Interface/X
License:        BSD
URL:            http://hackage.haskell.org/cgi-bin/hackage-scripts/package/%{name}
Source0:        http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:        xmonad.desktop
Source2:        xmonad-start
Patch0:         xmonad-config-manpage.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# fedora ghc archs:
ExclusiveArch: %{ix86} x86_64 ppc alpha
BuildRequires:  ghc
BuildRequires:  ghc-rpm-macros
BuildRequires:  ghc-X11-devel >= %{X11_version}
%if %{with doc}
BuildRequires:  ghc-doc
%endif
%if %{with prof}
BuildRequires:  ghc-prof, ghc-X11-prof >= %{X11_version}
%endif
Requires:       ghc-%{name}-devel = %{version}-%{release}
# required until there is a command to open some system default
# xterminal
Requires:       xterm
# for xmessage
Requires:       xorg-x11-apps

%description
xmonad is a tiling window manager for X. Windows are arranged
automatically to tile the screen without gaps or overlap, maximising
screen use. All features of the window manager are accessible from
the keyboard: a mouse is strictly optional. xmonad is written and
extensible in Haskell. Custom layout algorithms, and other
extensions, may be written by the user in config files. Layouts are
applied dynamically, and different layouts may be used on each
workspace. Xinerama is fully supported, allowing windows to be tiled
on several screens.


%package -n ghc-%{name}-devel
Summary:        Haskell %{name} library
Group:          Development/Libraries
Requires:       ghc-X11-devel >= %{X11_version}
Requires:       ghc = %{ghc_version}
Requires(post): ghc = %{ghc_version}
Requires(preun): ghc = %{ghc_version}

%description -n ghc-%{name}-devel
This package provides the Haskell %{name} library
built for ghc-%{ghc_version}.


%if %{with doc}
%package -n ghc-%{name}-doc
Summary:        Documentation for %{name}
Group:          Development/Libraries
Requires:       ghc-doc = %{ghc_version}
Requires(post): ghc-doc = %{ghc_version}
Requires(postun): ghc-doc = %{ghc_version}

%description -n ghc-%{name}-doc
This package contains development documentation files for the %{name} library.
%endif


%if %{with prof}
%package -n ghc-%{name}-prof
Summary:        Profiling libraries for %{name}
Group:          Development/Libraries
Requires:       ghc-%{name}-devel = %{version}-%{release}
Requires:       ghc-X11-prof >= %{X11_version}
Requires:       ghc-prof = %{ghc_version}

%description -n ghc-%{name}-prof
This package contains profiling libraries for %{name}.
%endif


%prep
%setup -q
%patch0 -p1 -b .orig

%build
%ifarch ppc
# hack around mysterious runghc fail
%global cabal ./cabal
ghc --make Setup -o cabal
%endif

%cabal_configure --ghc %{?with_prof:-p}
%cabal build
%if %{with doc}
%cabal haddock
%endif
%ghc_gen_scripts


%install
rm -rf $RPM_BUILD_ROOT
%cabal_install
%ghc_install_scripts
%ghc_gen_filelists ghc-%{name}

install -p -m 0644 -D man/%{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1
install -p -m 0644 -D %SOURCE1 $RPM_BUILD_ROOT%{_datadir}/xsessions/%{name}.desktop
install -p -m 0755 -D %SOURCE2 $RPM_BUILD_ROOT%{_bindir}/%{name}-start
install -p -m 0644 -D man/xmonad.hs $RPM_BUILD_ROOT%{_sysconfdir}/skel/.%{name}/%{name}.hs

%clean
rm -rf $RPM_BUILD_ROOT


%post -n ghc-%{name}-devel
%ghc_register_pkg


%if %{with doc}
%post -n ghc-%{name}-doc
%ghc_reindex_haddock
%endif


%preun -n ghc-%{name}-devel
if [ "$1" -eq 0 ] ; then
  %ghc_unregister_pkg
fi


%if %{with doc}
%postun -n ghc-%{name}-doc
if [ "$1" -eq 0 ] ; then
  %ghc_reindex_haddock
fi
%endif


%files
%defattr(-,root,root,-)
%doc CONFIG LICENSE README STYLE TODO man/%{name}.hs.orig
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-start
%{_mandir}/man1/%{name}.1*
%{_datadir}/xsessions/%{name}.desktop
%{_sysconfdir}/skel/.%{name}/%{name}.hs


%files -n ghc-%{name}-devel -f ghc-%{name}-devel.files
%defattr(-,root,root,-)


%if %{with doc}
%files -n ghc-%{name}-doc -f ghc-%{name}-doc.files
%defattr(-,root,root,-)
%endif


%if %{with prof}
%files -n ghc-%{name}-prof -f ghc-%{name}-prof.files
%defattr(-,root,root,-)
%endif


%changelog
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
