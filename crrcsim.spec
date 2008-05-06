#
# TODO:
# - lib64 support (Makefile.linux64 or patch for Makefile.linux)
# - addons - crrcsim-addon-models-0.2.0.zip
#
# Does not compile with glut:
# http://lists.pld-linux.org/mailman/pipermail/pld-devel-pl/2006-November/137392.html
#
# pulseaudio-devel > 18.1
# In file included from audio_interface/tx_audio.cpp:9:
# audio_interface/audio_rc.c: In function 'int audio_rc_open(T_TX_InterfaceAudio*)':
# audio_interface/audio_rc.c:251: error: 'Pa_GetCountDevices' was not declared in this scope
# audio_interface/audio_rc.c:265: error: 'Pa_GetDefaultInputDevice' was not declared in this scope
#
# Conditional build:
%bcond_with	debug		# build with debug
%bcond_with	sound		# build with sound

%define		_rel		2

Summary:	model-airplane flight simulator
#Summary(pl.UTF-8):
Name:		crrcsim
Version:	0.9.8
Release:	0.2
License:	GPL
Group:		X11/Applications/Games
Source0:	http://dl.sourceforge.net/crrcsim/%{name}-src-%{version}-%{_rel}.tar.gz
# Source0-md5:	c89b4458fe0697059d40a2e4636632d0
Source1:	%{name}.desktop
URL:		http:///crrcsim.sourceforge.net/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	freeglut-devel
BuildRequires:	gle-devel
BuildRequires:	glew-devel
#BuildRequires:	glut-devel = 3.7
BuildRequires:	pkg-config
%{?with_sound:BuildRequires:	pulseaudio-devel = 18.1}
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CRRCSim is a model-airplane flight simulation program for Linux with
ports to other platforms. Using CRRCSim you can learn how to fly model
aircraft, test new aircraft designs, and improve your skills by
practicing in the relative safety of your pc.

#%description -l pl.UTF-8


%prep
%setup -q -n %{name}-%{version}-%{_rel}

%if %{without sound}
%{__sed} -i 's/COMPILE_AUDIO_INTERFACE 1/COMPILE_AUDIO_INTERFACE 0/' crrc_config.h
%{__sed} -i 's/CRRC_LINKER_FLAGS += -lportaudio/#CRRC_LINKER_FLAGS += -lportaudio/' Makefile.linux
%endif

%{__sed} -i 's/\%{_prefix}\/local\/share\/games/$(DESTDIR)\%{_prefix}\/share/' Makefile.linux
%{__sed} -i 's/\%{_prefix}\/local/$(DESTDIR)\%{_prefix}/' Makefile.linux
%{__sed} -i 's/\%{_prefix}\/local\/share\/games/\%{_prefix}\/share/' config.cpp

%build
#cp -f /usr/share/automake/config.* admin
%{__make} -f Makefile.linux %{?with_debug:debug} \
	OPT_FLAGS="%{rpmcflags}" \
	CC_MODULE="%{__cc}" \
	CC="%{__cxx}" \
	CXX="%{__cxx}" \
	C++="%{__cxx}"

#%if "%{_lib}" == "lib64"
#	--enable-libsuffix=64 \
#%endif
#	--with-qt-libraries=%{_libdir}
#%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -f Makefile.linux install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_desktopdir}
install -d $RPM_BUILD_ROOT%{_pixmapsdir}
cp ./packages/icons/crrcsim.png $RPM_BUILD_ROOT%{_pixmapsdir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGES_BY_KL  CHANGES_BY_TT
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/%{name}
%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop
