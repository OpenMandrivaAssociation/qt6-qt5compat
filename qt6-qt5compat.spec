#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

%define libname %mklibname Qt6Core5Compat %{major}
%define devname %mklibname -d Qt6Core5Compat

Name:		qt6-qt5compat
Version:	6.10.1
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qt5compat-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		https://download.qt.io/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qt5compat-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt 5.x compatibility library for Qt %{major}
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	%{_lib}Qt%{major}Core-devel
BuildRequires:	%{_lib}Qt%{major}Gui-devel
BuildRequires:	%{_lib}Qt%{major}Network-devel
BuildRequires:	%{_lib}Qt%{major}Qml-devel
BuildRequires:	%{_lib}Qt%{major}QmlMeta-devel
BuildRequires:	%{_lib}Qt%{major}QmlModels-devel
BuildRequires:	%{_lib}Qt%{major}Quick-devel
BuildRequires:	%{_lib}Qt%{major}Xml-devel
BuildRequires:	%{_lib}Qt%{major}Widgets-devel
BuildRequires:	%{_lib}Qt%{major}Sql-devel
BuildRequires:	%{_lib}Qt%{major}PrintSupport-devel
BuildRequires:	%{_lib}Qt%{major}OpenGL-devel
BuildRequires:	%{_lib}Qt%{major}OpenGLWidgets-devel
BuildRequires:	%{_lib}Qt%{major}DBus-devel
BuildRequires:	cmake(Qt6ShaderTools)
BuildRequires:	qt%{major}-cmake
BuildRequires:	qt%{major}-qtdeclarative
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
License:	LGPLv3/GPLv3/GPLv2

%description
Qt 5.x compatibility library for Qt %{major}

%global extra_files_Core5Compat \
%{_qtdir}/qml/Qt5Compat

%global extra_devel_files_Core5Compat \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/*graphicaleffects* \
%{_qtdir}/lib/cmake/Qt6/FindWrapIconv.cmake \
%{_qtdir}/lib/cmake/Qt6BuildInternals/StandaloneTests/Qt5CompatTestsConfig.cmake \
%{_qtdir}/sbom/*

%qt6libs Core5Compat

%package examples
Summary: Examples for the Qt %{qtmajor} framework
Group: Documentation

%description examples
Documentation for the Qt %{qtmajor} framework

%files examples
%{_qtdir}/examples/core5

%prep
%autosetup -p1 -n qt5compat%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON \
	-DQT_MKSPECS_DIR:FILEPATH=%{_qtdir}/mkspecs

%build
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
