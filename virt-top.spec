%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%define debug_package %{nil}

Name:           virt-top
Version:        1.0.4
Release:        3.15%{?dist}
Summary:        Utility like top(1) for displaying virtualization stats

Group:          Development/Libraries
License:        GPLv2+
URL:            http://et.redhat.com/~rjones/virt-top/
Source0:        http://et.redhat.com/~rjones/virt-top/files/%{name}-%{version}.tar.gz

# Post-process output of CSV file (RHBZ#665817).
Source1:        processcsv.py
Source2:        processcsv.py.pod

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch:    sparc64 s390 s390x

Patch0:         virt-top-1.0.3-bogus-zh_CN-plurals.patch
Patch1:         virt-top-1.0.4-bogus-ja-plurals.patch

Patch2:         virt-top-1.0.4-man-page-memory-option-shows-total-guest-memory-RHBZ.patch
Patch3:         virt-top-1.0.4-Remove-references-to-xm-xentop-manual-pages-RHBZ-648.patch
Patch4:         virt-top-1.0.4-Document-background-noise-of-RX-packets-from-bridges.patch
Patch5:         virt-top-1.0.4-Fix-virt-top-end-time-option-when-TZ-UTC-RHBZ-637964.patch
Patch6:         virt-top-1.0.4-Fix-pad-function-to-work-for-negative-widths-RHBZ-63.patch
Patch7:         virt-top-1.0.4-main-Record-and-print-full-exception-stack-traces.patch
Patch8:         virt-top-1.0.4-Change-order-of-return-values-from-getyx-fixes-displ.patch
Patch9:         virt-top-1.0.4-Obey-virt-top-end-time-down-to-near-millisecond-accu.patch
Patch10:        virt-top-1.0.4-Add-stream-flag.patch
Patch11:        virt-top-1.0.4-Add-block-in-bytes-option.patch
Patch12:        virt-top-1.0.4-Fix-end-time-option-with-absolute-times.patch
Patch13:        virt-top-1.0.4-docs-Fix-documentation-for-virt-top-c-option.patch
Patch14:        virt-top-1.0.4-docs-Explain-how-to-debug-libvirt-initialization-pro.patch
Patch15:        virt-top-1.0.4-Record-memory-statistics-information-to-rd-object.patch
Patch16:        virt-top-1.0.4-add-memory-stats-to-csv-mode.patch
Patch17:        virt-top-1.0.4-processcsv-documentation.patch
Patch18:        virt-top-1.0.4-Fix-ordering-of-csv_mode-and-stream_mode-in-tuple.patch
Patch19:        virt-top-1.0.4-fix-virt-top-1.patch
Patch20:        virt-top-1.0.4-man-page-Update-copyright-date-and-link-to-web-pages.patch
Patch21:        virt-top-1.0.4-man-page-Update-copyright-date.patch
Patch22:        virt-top-1.0.4-Man-page-Add-an-explanation-of-columns-RHBZ-834208.patch
Patch23:        virt-top-1.0.4-Add-missing-sort-order-options-in-help-output-RHBZ-8.patch
Patch24:        virt-top-1.0.4-Better-error-messages-when-parsing-the-init-file-RHB.patch
Patch25:        virt-top-1.0.4-Rename-find_usages_from_stats-as-find_cpu_usages.patch
Patch26:        virt-top-1.0.4-show-vcpu-usages-by-virt-top-1.patch


BuildRequires:  ocaml >= 3.11.0
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-findlib-devel
# Need the ncurses / ncursesw (--enable-widec) fix.
BuildRequires:  ocaml-curses-devel >= 1.0.3-6.1
BuildRequires:  ocaml-extlib-devel
BuildRequires:  ocaml-xml-light-devel
BuildRequires:  ocaml-csv-devel
BuildRequires:  ocaml-calendar-devel
# Needs binding to virDomainGetCPUStats (RHBZ#737728).
BuildRequires:  ocaml-libvirt-devel >= 0.6.1.0-6.4

# Tortuous list of BRs for gettext.
BuildRequires:  ocaml-gettext-devel >= 0.3.3
BuildRequires:  ocaml-fileutils-devel
# For msgfmt:
BuildRequires:  gettext

# Non-OCaml BRs.
BuildRequires:  libvirt-devel
BuildRequires:  perl
BuildRequires:  gawk

# For execstack:
BuildRequires:  prelink


%description
virt-top is a 'top(1)'-like utility for showing stats of virtualized
domains.  Many keys and command line options are the same as for
ordinary 'top'.

It uses libvirt so it is capable of showing stats across a variety of
different virtualization systems.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
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
rm virt-top/virt-top.1
make -C virt-top virt-top.1

# Build processcsv.py.1.
pod2man -c "Virtualization Support" --release "%{name}-%{version}" \
  %{SOURCE2} > processcsv.py.1


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Install translations.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale
make -C po install PODIR="$RPM_BUILD_ROOT%{_datadir}/locale"
%find_lang %{name}

# Install virt-top manpage by hand for now.
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 0644 virt-top/virt-top.1 $RPM_BUILD_ROOT%{_mandir}/man1

# Clear executable stack flag.  Really this is a bug in the OCaml
# compiler on ppc, but it's simpler to just clear the bit here for all
# architectures.
# https://bugzilla.redhat.com/show_bug.cgi?id=605124
# http://caml.inria.fr/mantis/view.php?id=4564
execstack -c $RPM_BUILD_ROOT%{_bindir}/virt-top

# Install processcsv.py.
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

# Install processcsv.py(1).
install -m 0644 processcsv.py.1 $RPM_BUILD_ROOT%{_mandir}/man1/


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README TODO.virt-top ChangeLog
%{_bindir}/processcsv.py
%{_bindir}/virt-top
%{_mandir}/man1/processcsv.py.1*
%{_mandir}/man1/virt-top.1*


%changelog
* Fri Oct 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.15
- Split out hypervisor + domain pCPU usage from domain-only pCPU usage.
  resolves: rhbz#841759

* Fri Sep 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.14
- Fix the copyright date and a link in the man page.
  resolves: rhbz#825627
- Add an explanation of columns.
  resolves: rhbz#834208
- Add missing sort order options in help output.
  resolves: rhbz#807176
- Better error messages when parsing the init file.
  resolves: rhbz#836231
- Write and install a specific man page for processcsv.py.
  resolves: rhbz#835547

* Fri Mar 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.13
- Rebuild against fixed virDomainGetCPUStats binding in ocaml-libvirt.
  resolves: RHBZ#737728

* Tue Mar  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.12
- Fix virt-top -1 to use virDomainGetCPUStats.
  resolves: RHBZ#737728

* Fri Aug 12 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.11
- Fix ordering of csv_mode and stream_mode in tuple.
  resolves: RHBZ#730208

* Thu Aug 11 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.10
- docs: Explain how to debug libvirt initialization problems
  resolves: RHBZ#680031
- Show domain memory information in csv mode.
  resolves: RHBZ#680027
- Add processcsv.py file and documentation.
  resolves: RHBZ#665817

* Tue Mar  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.8
- Fix --end-time option with absolute times.
  resolves: RHBZ#680344
- Fix documentation for virt-top -c option.
  resolves: RHBZ#676979

* Fri Feb  4 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.7
- Add --stream and --block-in-bytes options from Fujitsu.
  resolves: RHBZ#643893

* Wed Jan 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.6
- Obey virt-top --end-time down to near millisecond accuracy
  resolves: RHBZ#637964

* Mon Jan 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.5
- Clear executable stack bit on PPC (RHBZ#605124).

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.4
- Fix location of historical %%CPU on virt-top (RHBZ#629500).

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.3
- Drop ocaml-camomile* dependency (RHBZ#661783).
- Document background noise of RX packets from bridges (RHBZ#647987).
- Fix pad function to work for negative widths (RHBZ#634435).
- Fix virt-top --end-time option when TZ<>UTC (RHBZ#637964).
- Document that memory option shows total guest memory (RHBZ#647991).
- Remove references to xm/xentop manual pages (RHBZ#648186).
- Record and print full exception stack traces to aid debugging.
  This also requires OCaml 3.11.0 so update BR.

* Mon Jan 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3.1
- Import package from Fedora Rawhide.

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

* Tue Mar 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.1-1
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
