%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           virt-top
Version:        1.0.8
Release:        7%{?dist}
Summary:        Utility like top(1) for displaying virtualization stats

License:        GPLv2+
URL:            http://people.redhat.com/~rjones/virt-top/
Source0:        http://people.redhat.com/~rjones/virt-top/files/%{name}-%{version}.tar.gz

%if 0%{?rhel} >= 6
# Post-process output of CSV file (RHBZ#665817, RHBZ#912020).
Source1:        processcsv.py
Source2:        processcsv.py.pod

Patch0:         virt-top-1.0.4-processcsv-documentation.patch
%endif

# Update configure for aarch64 (bz #926701)
Patch1: virt-top-aarch64.patch
ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.2
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-findlib-devel
# Need the ncurses / ncursesw (--enable-widec) fix.
BuildRequires:  ocaml-curses-devel >= 1.0.3-7
BuildRequires:  ocaml-extlib-devel
BuildRequires:  ocaml-xml-light-devel
BuildRequires:  ocaml-csv-devel
BuildRequires:  ocaml-calendar-devel
# Need support for virDomainGetCPUStats (fixed in 0.6.1.2).
BuildRequires:  ocaml-libvirt-devel >= 0.6.1.2-5

# Tortuous list of BRs for gettext.
BuildRequires:  ocaml-gettext-devel >= 0.3.3
BuildRequires:  ocaml-fileutils-devel
# For msgfmt:
BuildRequires:  gettext

# Non-OCaml BRs.
BuildRequires:  libvirt-devel
BuildRequires:  perl
BuildRequires:  perl(Pod::Perldoc)
BuildRequires:  gawk

%ifarch ppc ppc64
BuildRequires:  /usr/bin/execstack
%endif


%description
virt-top is a 'top(1)'-like utility for showing stats of virtualized
domains.  Many keys and command line options are the same as for
ordinary 'top'.

It uses libvirt so it is capable of showing stats across a variety of
different virtualization systems.


%prep
%setup -q

%if 0%{?rhel} >= 6
%patch0 -p1
%endif

# Update configure for aarch64 (bz #926701)
%patch1 -p1

chmod -x COPYING


%build
%configure
make all
%if %opt
make opt
strip virt-top/virt-top.opt
%endif

# Build translations.
make -C po

# Force rebuild of man page.
rm -f virt-top/virt-top.1
make -C virt-top virt-top.1

%if 0%{?rhel} >= 6
# Build processcsv.py.1.
pod2man -c "Virtualization Support" --release "%{name}-%{version}" \
  %{SOURCE2} > processcsv.py.1
%endif


%install
make DESTDIR=$RPM_BUILD_ROOT install

# Install translations.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale
make -C po install PODIR="$RPM_BUILD_ROOT%{_datadir}/locale"
%find_lang %{name}

# Install virt-top manpage by hand for now.
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 0644 virt-top/virt-top.1 $RPM_BUILD_ROOT%{_mandir}/man1

%ifarch ppc ppc64
# Clear executable stack flag.  Really this is a bug in the OCaml
# compiler on ppc, but it's simpler to just clear the bit here for all
# architectures.
# https://bugzilla.redhat.com/show_bug.cgi?id=605124
# http://caml.inria.fr/mantis/view.php?id=4564
execstack -c $RPM_BUILD_ROOT%{_bindir}/virt-top
%endif

%if 0%{?rhel} >= 6
# Install processcsv.py.
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

# Install processcsv.py(1).
install -m 0644 processcsv.py.1 $RPM_BUILD_ROOT%{_mandir}/man1/
%endif


%files -f %{name}.lang
%doc COPYING README TODO ChangeLog
%{_bindir}/virt-top
%{_mandir}/man1/virt-top.1*
%if 0%{?rhel} >= 6
%{_bindir}/processcsv.py
%{_mandir}/man1/processcsv.py.1*
%endif


%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.8-7
- Mass rebuild 2013-12-27

* Mon Jul 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-6
- Include processcsv.py script and man page, but on RHEL only
  (RHBZ#665817, RHBZ#912020)
- Clear executable stack flag on PPC, PPC64 (RHBZ#605124).

* Fri Jun 28 2013 Cole Robinson <crobinso@redhat.com> - 1.0.8-5
- Update configure for aarch64 (bz #926701)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-3
- Rebuild for OCaml 4.00.1.

* Fri Oct 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-2
- New upstream version 1.0.8.
- Requires tiny change to ocaml-libvirt, hence dep bump.
- Clean up the spec file.
- Remove explicit BR ocaml-camomile (not used AFAIK).

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.7-2
- Require fixed ocaml-libvirt.

* Tue Mar  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.7-1
- New upstream version 1.0.7.
- Includes true physical CPU reporting (when libvirt supports this).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 12 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.6-1
- New upstream version 1.0.6.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.5-1
- New upstream version 1.0.5.
- Rebuild against OCaml 3.12.0.
- Project website moved to people.redhat.com.
- Remove upstream patches.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3
- Force rebuild against latest ocaml-gettext 0.3.3 (RHBZ#508197#c10).

* Mon Oct  5 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-2
- New upstream release 1.0.4.
- Includes new translations (RHBZ#493799).
- Overall hardware memory is now displayed in CSV file (RHBZ#521785).
- Several fixes to Japanese support (RHBZ#508197).
- Japanese PO file also has bogus plural forms.
- Additional BR on gettext (for msgfmt).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-3
- Rebuild for OCaml 3.11.0+rc1.

* Tue Oct 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-2
- Fix incorrect sources file.
- Remove bogus Plural-Forms line from zh_CN PO file.

* Tue Oct 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-1
- New upstream version 1.0.3.

* Mon May 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-2
- Use RPM percent-configure.
- Add list of BRs for gettext.
- Use find_lang to find PO files.
- Comment out the OCaml dependency generator.  Not a library so not
  needed.

* Thu May  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-1
- New upstream release 1.0.1.
- Don't BR ocaml-gettext-devel, it's not used at the moment.
- Don't gzip the manpage, it happens automatically.
- Add BR libvirt-devel.
- Remove spurious executable bit on COPYING.

* Thu Apr 17 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-2
- New upstream release 1.0.0.
- Force rebuild of manpage.

* Tue Mar 18 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.1-1
- New upstream release 0.4.1.1.
- Move configure to build section.
- Pass RPM_OPT_FLAGS.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.0-2
- Fix source URL.
- Install virt-df manpage.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.0-1
- New upstream release 0.4.1.0.
- Upstream now requires ocaml-dbus >= 0.06, ocaml-lablgtk >= 2.10.0,
  ocaml-dbus-devel.
- Enable virt-df.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-3
- Rebuild for ppc64.

* Wed Feb 13 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-2
- Add BR gtk2-devel

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-1
- New upstream version 0.4.0.3.
- Rebuild for OCaml 3.10.1.

* Tue Nov 20 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.4-1
- New upstream release 0.3.3.4.
- Upstream website is now http://libvirt.org/ocaml/

* Fri Oct 19 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.0-2
- Mistake: BR is ocaml-calendar-devel.

* Fri Oct 19 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.0-1
- New upstream release 0.3.3.0.
- Added support for virt-df, but disabled it by default.
- +BR ocaml-calendar.

* Mon Sep 24 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.8-1
- New upstream release 0.3.2.8.

* Thu Sep 20 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.7-1
- New upstream release 0.3.2.7.
- Ship the upstream ChangeLog file.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.6-2
- Force dependency on ocaml >= 3.10.0-7 which has fixed requires/provides
  scripts.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.6-1
- New upstream version 0.3.2.6.

* Wed Aug 29 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.5-1
- New upstream version 0.3.2.5.
- Keep TODO out of the main package, but add (renamed) TODO.libvirt and
  TODO.virt-top to the devel and virt-top packages respectively.
- Add BR gawk.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.4-1
- New upstream version 0.3.2.4.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.3-2
- build_* macros so we can choose what subpackages to build.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.3-1
- Upstream version 0.3.2.3.
- Add missing BR libvirt-devel.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.2-1
- Upstream version 0.3.2.2.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.1-2
- Fix unclosed if-statement in spec file.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.1-1
- Upstream version 0.3.2.1.
- Put HTML documentation in -devel package.

* Mon Aug  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.1.2-1
- Initial RPM release.
