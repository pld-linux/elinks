Summary:	Experimantal Links (text WWW browser)
Summary(es):	El links es un browser para modo texto, similar a lynx
Summary(pl):	Eksperymentalny Links (tekstowa przegl±darka WWW)
Summary(pt_BR):	O links é um browser para modo texto, similar ao lynx
Name:		elinks
Version:	0.4.1
Release:	1
Epoch:		1
License:	GPL
Group:		Applications/Networking
Source0:	http://elinks.or.cz/download/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Source2:	links.png
URL:		http://elinks.or.cz/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	expat-devel
BuildRequires:	gpm-devel
BuildRequires:	lua40-devel
BuildRequires:	ncurses-devel => 5.1
BuildRequires:	openssl-devel >= 0.9.6a
BuildRequires:	zlib-devel
BuildRequires:	/usr/bin/texi2html
Provides:	webclient
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the elinks tree - intended to provide feature-rich version of
links, however not rock-stable and dedicated mainly for testing. Its
purpose is to make alternative to links, until Mikulas will have some
time to maintain it, and to test and tune various patches for Mikulas
to be able to include them in the official links releases.

%description -l es
Links es un browser WWW modo texto, similar al Lynx. El links muestra
tablas, hace baja archivos en segundo plano, y usa conexiones HTTP/1.1
keepalive.

%description -l pl
Bogata w opcje i mo¿liwo¶ci wersja tekstowej przegl±darki www - links.
elinks jednak jest dedykowana g³ównie do testowania.

%description -l pt_BR
Links é um browser WWW modo texto, similar ao Lynx. O Links exibe
tabelas, baixa arquivos em segundo plano, e usa as conexões HTTP/1.1
keepalive.

%prep
%setup -q

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-fastmem \
	--without-x
%{__make}

cd doc
texi2html elinks-lua.texi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW \
	$RPM_BUILD_ROOT%{_datadir}/%{name} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_pixmapsdir}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

install contrib/lua/*.lua $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README SITES TODO
%doc contrib/{completion.tcsh,keybind*,wipe-out-ssl*,lua/elinks-remote}
%doc contrib/conv/{*awk,*.pl,*.sh}
%doc doc/{*.txt,*.html}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man*/*
%{_applnkdir}/Network/WWW/*
%{_pixmapsdir}/*
