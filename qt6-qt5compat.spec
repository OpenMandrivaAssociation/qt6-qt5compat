#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

%define libname %mklibname Qt6Core5Compat %{major}
%define devname %mklibname -d Qt6Core5Compat

Name:		qt6-qt5compat
Version:	6.2.2
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qt5compat-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qt5compat-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt 5.x compatibility library for Qt %{major}
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	%{_lib}Qt%{major}Core-devel
BuildRequires:	%{_lib}Qt%{major}Gui-devel
BuildRequires:	%{_lib}Qt%{major}Network-devel
BuildRequires:	%{_lib}Qt%{major}Qml-devel
BuildRequires:	%{_lib}Qt%{major}QmlDevTools-devel
BuildRequires:	%{_lib}Qt%{major}QmlModels-devel
BuildRequires:	%{_lib}Qt%{major}Quick-devel
BuildRequires:	%{_lib}Qt%{major}Xml-devel
BuildRequires:	%{_lib}Qt%{major}Widgets-devel
BuildRequires:	%{_lib}Qt%{major}QmlDevTools-devel
BuildRequires:	%{_lib}Qt%{major}Sql-devel
BuildRequires:	%{_lib}Qt%{major}PrintSupport-devel
BuildRequires:	%{_lib}Qt%{major}OpenGL-devel
BuildRequires:	%{_lib}Qt%{major}OpenGLWidgets-devel
BuildRequires:	%{_lib}Qt%{major}DBus-devel
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
# Not really required, but referenced by LLVMExports.cmake
# (and then required because of the integrity check)
BuildRequires:	%{_lib}gpuruntime
License:	LGPLv3/GPLv3/GPLv2

%description
Qt 5.x compatibility library for Qt %{major}

%package -n %{libname}
Summary:	Qt 5.x compatibility library for Qt %{major}

%description -n %{libname}
Qt 5.x compatibility library for Qt %{major}

%package -n %{devname}
Summary:	Development files for the Qt 5.x compatibility library for Qt %{major}
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files for the Qt 5.x compatibility library for Qt %{major}

%prep
%autosetup -p1 -n qt5compat%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
# FIXME why are OpenGL lib paths autodetected incorrectly, preferring
# /usr/lib over /usr/lib64 even on 64-bit boxes?
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
# Static helper lib without headers -- useless
rm -f %{buildroot}%{_libdir}/qt6/%{_lib}/libpnp_basictools.a
# Put stuff where tools will find it
# We can't do the same for %{_includedir} right now because that would
# clash with qt5 (both would want to have /usr/include/QtCore and friends)
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_libdir}/cmake
for i in %{buildroot}%{_qtdir}/lib/*.so*; do
	ln -s qt%{major}/lib/$(basename ${i}) %{buildroot}%{_libdir}/
done
mv %{buildroot}%{_qtdir}/lib/cmake %{buildroot}%{_libdir}/

%files -n %{libname}
%{_libdir}/libQt6Core5Compat.so.*
%{_qtdir}/lib/libQt6Core5Compat.so.*

%files -n %{devname}
%{_libdir}/cmake/Qt6Core5Compat
%{_libdir}/cmake/Qt6BuildInternals/StandaloneTests/*.cmake
%{_libdir}/cmake/Qt6/FindWrapIconv.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectspluginAdditionalTargetInfo.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectspluginConfig.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectspluginConfigVersion.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectspluginConfigVersionImpl.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectspluginTargets-relwithdebinfo.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectspluginTargets.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectsprivateAdditionalTargetInfo.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectsprivateConfig.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectsprivateConfigVersion.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectsprivateConfigVersionImpl.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectsprivateTargets-relwithdebinfo.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtgraphicaleffectsprivateTargets.cmake
%{_libdir}/libQt6Core5Compat.so
%{_qtdir}/include/QtCore5Compat
%{_qtdir}/lib/libQt6Core5Compat.prl
%{_qtdir}/lib/libQt6Core5Compat.so
%{_qtdir}/mkspecs/modules/qt_lib_core5compat.pri
%{_qtdir}/mkspecs/modules/qt_lib_core5compat_private.pri
%{_qtdir}/modules/Core5Compat.json
%{_qtdir}/qml/Qt5Compat
%{_qtdir}/lib/metatypes/qt6core5compat_relwithdebinfo_metatypes.json
