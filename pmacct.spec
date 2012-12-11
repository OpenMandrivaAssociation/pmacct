%define with_pgsql       0
%define with_sqlite      0

Summary: Promiscuous mode IP Accounting package
Name: pmacct
Version: 0.12.5
Release: %mkrel 0
License: GPL
Group: Monitoring
Source: http://www.pmacct.net/%{name}-%{version}.tar.gz
Source1: nfacctd.init
Source2: pmacctd.init
Source3: sfacctd.init
Source4: sfacctd.conf
Patch1: pmacct-fix_realloc.patch
URL: http://www.pmacct.net/
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: mysql-devel
%if %{with_pgsql}
BuildRequires: postgresql-devel
%endif
%if %{with_sqlite}
BuildRequires: sqlite-devel >= 3.0.0
%endif
BuildRequires: libpcap-devel

%description
pmacct is a small set of passive network monitoring tools to measure, account,
classify and aggregate IPv4 and IPv6 traffic; a pluggable and flexible
architecture allows to store the collected traffic data into memory tables or
SQL (MySQL, SQLite, PostgreSQL) databases. pmacct supports fully customizable
historical data breakdown, flow sampling, filtering and tagging, recovery
actions, and triggers. Libpcap, sFlow v2/v4/v5 and NetFlow v1/v5/v7/v8/v9 are
supported, both unicast and multicast. Also, a client program makes it easy to
export data to tools like RRDtool, GNUPlot, Net-SNMP, MRTG, and Cacti.

%prep
%setup -q
%patch1
chmod a+rx docs examples sql
find docs examples sql -type f -print0 | xargs -r0 chmod -x

%build
%configure \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --enable-threads \
    --enable-64bit \
    --enable-mysql \
%if %{with_pgsql}
    --enable-pgsql \
    --with-pgsql-includes=/usr/include/pgsql/ \
%endif
%if %{with_sqlite}
    --enable-sqlite3 \
%endif
    --enable-ulog \
    --enable-ipv6 \
    --enable-v4-mapped


%__make %{?jobs:-j%{jobs}}

%install
%makeinstall

%{__install} -Dp %{SOURCE1} %{buildroot}/%{_sysconfdir}/init.d/nfacctd
%{__install} -Dp %{SOURCE2} %{buildroot}/%{_sysconfdir}/init.d/pmacctd
%{__install} -Dp %{SOURCE3} %{buildroot}/%{_sysconfdir}/init.d/sfacctd
ln -sf ../../etc/init.d/nfacctd $RPM_BUILD_ROOT/usr/sbin/rcnfacctd
ln -sf ../../etc/init.d/pmacctd $RPM_BUILD_ROOT/usr/sbin/rcpmacctd
ln -sf ../../etc/init.d/sfacctd $RPM_BUILD_ROOT/usr/sbin/rcsfacctd

%{__install} -Dp examples/nfacctd-sql_v2.conf.example %{buildroot}/%{_sysconfdir}/pmacct/nfacctd.conf
%{__install} -Dp examples/pmacctd-sql_v2.conf.example %{buildroot}/%{_sysconfdir}/pmacct/pmacctd.conf
%{__install} -Dp %{SOURCE4} %{buildroot}/%{_sysconfdir}/pmacct/sfacctd.conf

rm -f $RPM_BUILD_ROOT/usr/sbin/rc*acctd

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog CONFIG-KEYS COPYING EXAMPLES FAQS INSTALL KNOWN-BUGS NEWS README TODO TOOLS UPGRADE
%doc docs examples sql
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_sysconfdir}/init.d/*
%dir /etc/pmacct
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/pmacct/nfacctd.conf
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/pmacct/pmacctd.conf
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/pmacct/sfacctd.conf


%changelog
* Thu Mar 24 2011 zamir <zamir@mandriva.org> 0.12.5-0mdv2011.0
+ Revision: 648360
- first build
- create pmacct

