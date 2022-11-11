# (tpg) https://github.com/ARM-software/astc-encoder/issues/387
%global optflags %{optflags} -O3 -DASTCENC_DYNAMIC_LIBRARY=1 -Wno-error=array-parameter

Summary:	ARM Adaptive Scalable Texture Compression (ASTC) Encoder
Name:		astc-encoder
Version:	4.2.0
Release:	1
License:	APL
Group:		System/Libraries
URL:		https://github.com/ARM-software/astc-encoder
Source0:	https://github.com/ARM-software/astc-encoder/archive/refs/tags/%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	ninja
Provides:	astcenc

%description
ARM Adaptive Scalable Texture Compression (ASTC) Encoder,
astcenc, a command-line tool for compressing and decompressing
images using the ASTC texture compression standard.

%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{EVRD}

%description devel
Development files for %{name}.

%prep
%autosetup -p1

%cmake \
%ifarch aarch64
	-DISA_NEON=ON \
%endif
%ifarch %{x86_64}
	-DISA_AVX2=ON \
	-DISA_SSE41=ON \
	-DISA_SSE2=ON \
%endif
	-DNO_INVARIANCE=ON \
	-DCLI=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

mkdir -p %{buildroot}{%{_libdir},%{_includedir}}

cp -a build/Source/libastcenc*.a %{buildroot}%{_libdir}/
cp -p Source/astcenc.h %{buildroot}%{_includedir}/

%files
%{_bindir}/astcenc-*

%files devel
%{_includedir}/*.h
%{_libdir}/*.a
