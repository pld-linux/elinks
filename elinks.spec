Summary:	Experimantal Links (text WWW browser)
Summary(pl):	Eksperymentalny Links (tekstowa przegl±darka WWW)
Name:		elinks
Version:	0.4pre19
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://elinks.or.cz/download/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Source2:	links.png
#Patch0:		%{name}-configure.patch
URL:		http://elinks.or.cz/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	gpm-devel
BuildRequires:	lua40-devel
BuildRequires:	ncurses-devel => 5.1
BuildRequires:	openssl-devel >= 0.9.6a
BuildRequires:	zlib-devel
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
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--without-x
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW \
	$RPM_BUILD_ROOT%{_datadir}/%{name} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_pixmapsdir}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

install contrib/lua/config.lua $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog HACKING LUA NEWS README SITES TODO
%doc contrib/{completion.tcsh,keybind*,wipe-out-ssl*,lua/{*.lua,elinks-remote}}
%doc contrib/conv/{*awk,*.pl,*.sh}
%attr(755,root,root) %{_bindir}/*
%{_applnkdir}/Network/WWW/*
%{_mandir}/man*/*
%{_pixmapsdir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}
