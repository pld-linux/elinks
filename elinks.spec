%define snap	20020208 
Summary:	Experimantal Links (text WWW browser)
Summary(pl):	Eksperymentalne Links (tekstowa przegl±darka WWW)
Name:		elinks
Version:	0.2.3
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://pasky.ji.cz/elinks/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Source2:	%{name}-bm.lua
Source3:	%{name}-hooks.lua
Patch0:		%{name}-configure.patch
Patch1:		%{name}-lua-config-file.patch
URL:		http://pasky.ji.cz/elinks/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel => 5.1
BuildRequires:	openssl-devel >= 0.9.6a
BuildRequires:	lua-devel
Provides:	webclient
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the elinks tree - intended to provide feature-rich version of
links, however not rock-stable and dedicated mainly for testing. Its
purpose is to make alternative to links, until Mikulas will have some
time to maintain it, and to test and tune various patches for Mikulas
to be able to include them in the official links releases.

%description -l pl
Bogata w opcje i mo¿liwo¶ci wersja tekstowej przegl±darki www - links.
elinks jednak jest dedykowana g³ównie do testowania.

%prep
%setup -q -n %{name}-%{snap}
%patch0 -p1
%patch1 -p1

%build
rm -f missing
aclocal
autoconf
automake -a -c
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_bindir}/links		$RPM_BUILD_ROOT%{_bindir}/%{name}
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/links.1	$RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}

gzip -9nf AUTHORS BUGS ChangeLog README SITES TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_applnkdir}/Network/WWW/*
%{_mandir}/man*/*
%{_datadir}/%{name}/*
%{_sysconfdir}/*
