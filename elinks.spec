# TODO: consider lua51

# Conditional build:
%bcond_with	gnutls		# Enable GNUTLS SSL support (disables openssl)
%bcond_with	lzma		# Enable lzma support
%bcond_with	python		# Enable Python scripting support
%bcond_with	ruby		# Enable (experimental) Ruby scripting support
%bcond_with	smb		# Enable smb protocol support (smb requires libsmbclient)
#The latest libsmbclient is GPLv3, while ELinks is GPL v2 only.
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	x		# Use the X Windows System
%bcond_without	256		# Disable 256 colors support
%bcond_without	bittorrent	# Disable BitTorrent support
%bcond_without	cgi		# Disable Local CGI support
%bcond_without	fsp		# Disable FSP support
%bcond_without	guile		# Disable Guile scripting
%bcond_without	idn		# Disable Internation Domain Names support
%bcond_without	ipv6		# Disable IPv6 support
%bcond_without	js		# Disable experimental (yet quite usable) JavaScript support (using SpiderMonkey)
%bcond_without	led		# Disable LEDs
%bcond_without	lua		# Disable Lua scripting
%bcond_without	openssl		# Disable OpenSSL support
%bcond_without	perl		# Disable Perl scripting
# 
%if %{with gnutls}
%undefine	with_openssl
%endif
#
%define		pre	pre5
Summary:	Experimantal Links (text WWW browser)
Summary(es.UTF-8):	El links es un browser para modo texto, similar a lynx
Summary(pl.UTF-8):	Eksperymentalny Links (tekstowa przeglądarka WWW)
Summary(pt_BR.UTF-8):	O links é um browser para modo texto, similar ao lynx
Name:		elinks
Version:	0.12
Release:	0.%{pre}.2
Epoch:		1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://www.elinks.cz/download/%{name}-%{version}%{pre}.tar.bz2
# Source0-md5:	92790144290131ac5e63b44548b45e08
Source1:	%{name}.desktop
Source2:	links.png
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-lua40.patch
Patch2:		%{name}-date-format.patch
Patch3:		%{name}-old_incremental.patch
Patch4:		%{name}-fbterm.patch
URL:		http://www.elinks.cz/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	expat-devel
%{?with_fsp:BuildRequires:	fsplib-devel}
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel
%{?with_guile:BuildRequires: guile-devel}
%{?with_gnutls:BuildRequires: gnutls-devel >= 1.2.5}
%{?with_js:BuildRequires:	js-devel >= 1.5-0.rc6a.1}
%{?with_idn:BuildRequires:	libidn-devel}
%{?with_smb:BuildRequires:	libsmbclient-devel}
%{?with_lua:BuildRequires:	lua50-devel}
%{?with_lzma:BuildRequires:	lzma-devel}
BuildRequires:	ncurses-devel >= 5.1
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_perl:BuildRequires:	perl-devel}
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python-devel}
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	tre-devel
BuildRequires:	which
BuildRequires:	zlib-devel
Suggests:	mailcap
Provides:	webclient
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/elinks
%define		specflags_ia32	-fomit-frame-pointer 

%description
This is the elinks tree - intended to provide feature-rich version of
links, however not rock-stable and dedicated mainly for testing. Its
purpose is to make alternative to links, until Mikulas will have some
time to maintain it, and to test and tune various patches for Mikulas
to be able to include them in the official links releases.

%description -l es.UTF-8
Links es un browser WWW modo texto, similar al Lynx. El links muestra
tablas, hace baja archivos en segundo plano, y usa conexiones HTTP/1.1
keepalive.

%description -l pl.UTF-8
Bogata w opcje i możliwości wersja tekstowej przeglądarki WWW - links.
elinks jednak jest dedykowana głównie do testowania.

%description -l pt_BR.UTF-8
Links é um browser WWW modo texto, similar ao Lynx. O Links exibe
tabelas, baixa arquivos em segundo plano, e usa as conexões HTTP/1.1
keepalive.

%prep
%setup -q -n %{name}-%{version}%{pre}
%patch0 -p1
%patch1 -p1
%patch2 -p1
# restores old behaviour of type-ahead search
#%patch3 -p1
%patch4 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	%{?with_smb:--enable-smb} \
	--disable-no-root \
	%{!?debug:--enable-fastmem} \
	%{?debug:--enable-debug} \
	%{!?with_ipv6:--disable-ipv6} \
	%{?with_bittorrent:--enable-bittorrent} \
	%{?with_cgi:--enable-cgi} \
	--enable-finger \
	--enable-gopher \
	--enable-nntp \
	%{?with_256:--enable-256-colors} \
	--enable-exmode \
	%{?with_fsp:--enable-fsp} \
	%{?with_leds:--enable-leds} \
	--enable-marks \
	--enable-html-highlight \
	%{!?with_idn:--without-idn} \
	%{?with_guile:--with-guile} \
	%{?with_perl:--with-perl} \
	%{!?with_lua:--without-lua} \
	%{?with_python:--with-python} \
	%{?with_ruby:--with-ruby} \
	%{!?with_js:--without-spidermonkey} \
	%{?with_gnutls:--with-gnutls} \
	%{!?with_openssl:--without-openssl} \
	--with%{!?with_x:out}-x \
	%{!?with_lzma:--without-lzma}
# xterm -e is default, one might want to change it to
# something else
#	--with-xterm="xterm -e"

%{__make} %{?with_verbose:V=1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_datadir}/%{name} \
	$RPM_BUILD_ROOT{%{_sysconfdir},%{_pixmapsdir}}

%{__make} install %{?with_verbose:V=1} \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%{?with_lua:install contrib/lua/*.lua $RPM_BUILD_ROOT%{_sysconfdir}}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README SITES TODO
%doc contrib/{keybind*,wipe-out-ssl*,lua/elinks-remote}
%doc contrib/conv/{*awk,*.pl,*.sh}
%doc doc/html/*.html
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man*/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%{?with_lua:%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}}
