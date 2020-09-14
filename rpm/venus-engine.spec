##############################################################
# http://www.rpm.org/max-rpm/ch-rpm-inside.html              #
##############################################################
Name: venus-engine
Version:1.0.11
Release: %(echo $RELEASE)%{?dist}
# if you want use the parameter of rpm_create on build time,
# uncomment below
Summary: venus engine
Group: alibaba/application
License: Commercial
%define _prefix /usr/local/venus



# uncomment below, if your building depend on other packages

#BuildRequires: package_name = 1.0.0

# uncomment below, if depend on other packages

#Requires: package_name = 1.0.0


%description
# if you want publish current svn URL or Revision use these macros
venus engine
CodeUrl:%{_source_path}
CodeRev:%{_source_revision}

%debug_package
# support debuginfo package, to reduce runtime package size

# prepare your files
%install
# OLDPWD is the dir of rpm_create running
# _prefix is an inner var of rpmbuild,
# can set by rpm_create, default is "/home/a"
# _lib is an inner var, maybe "lib" or "lib64" depend on OS

# create dirs
mkdir -p $RPM_BUILD_ROOT%{_prefix}

#copy *.py to install path
echo $OLDPWD
cd $OLDPWD/..;
cp com $RPM_BUILD_ROOT%{_prefix} -rf;
cp config $RPM_BUILD_ROOT%{_prefix} -rf;
cp *.py $RPM_BUILD_ROOT%{_prefix};
cp README.md $RPM_BUILD_ROOT%{_prefix};

#build cpp and copy to install path
echo $OLDPWD
cd $OLDPWD/../../../cpp/;
mkdir -p build;
cd build;
cmake ..;make;make install DESTDIR=.
cp .%{_prefix}/* $RPM_BUILD_ROOT%{_prefix}/ -rf

#copy third lib to install path
echo $OLDPWD
cd $OLDPWD/../cpp/libs/third_lib/lib;
cp */lib* $RPM_BUILD_ROOT%{_prefix}/lib64 -df

cd ${RPM_BUILD_ROOT}
find -type f > ../file.list && sed -i "s/^\.//" ../file.list

#cd $OLDPWD/../;
# make %{_smp_mflags};
# make install DESTDIR=${RPM_BUILD_ROOT}%{_prefix};

# create a crontab of the package
#echo "
#* * * * * root /home/a/bin/every_min
#3 * * * * ads /home/a/bin/every_hour
#" > %{_crontab}

# package infomation
%files
# set file attribute here
%defattr(-,root,root)
# need not list every file here, keep it as this
%{_prefix}
## create an empy dir

# %dir %{_prefix}/var/log

## need bakup old config file, so indicate here

## %config %{_prefix}/etc/sample.conf

## or need keep old config file, so indicate with "noreplace"

## %config(noreplace) %{_prefix}/etc/sample.conf

## indicate the dir for crontab

## %attr(644,root,root) %{_crondir}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Mon Dec 30 2019 cy187263
- add spec of venus_engine
