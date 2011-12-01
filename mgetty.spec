%define date Jun15
%define SENDFAX_UID 78

Summary: A getty replacement for use with data and fax modems
Name: mgetty
Version: 1.1.36
Release: 8%{?dist}
Source: ftp://mgetty.greenie.net/pub/mgetty/source/1.1/mgetty%{version}-%{date}.tar.gz
Source1: ftp://mgetty.greenie.net/pub/mgetty/source/1.1/mgetty%{version}-%{date}.tar.gz.asc
Source2: logrotate.mgetty
Source3: logrotate.sendfax
Source4: logrotate.vgetty
Source5: logrotate.vm
Patch0: mgetty-1.1.29-config.patch
Patch1: mgetty-1.1.26-policy.patch
Patch4: mgetty-1.1.25-voiceconfig.patch
Patch5: mgetty-1.1.26-issue.patch
Patch6: mgetty-1.1.31-issue-doc.patch
Patch7: mgetty-1.1.29-helper.patch
Patch8: mgetty-1.1.30-mktemp.patch
Patch9: mgetty-1.1.30-unioninit.patch
Patch11: mgetty-1.1.31-helper2.patch
Patch12: mgetty-1.1.31-no-acroread.patch
Patch14: mgetty-1.1.31-sendmail_path.patch
Patch15: mgetty-1.1.31-lfs.patch
Patch16: mgetty-1.1.31-162174_tcflush.patch
Patch18: mgetty-1.1.33-bug_63843.patch
Patch19: mgetty-1.1.33-167830_tty_access.patch
Patch20: mgetty-1.1.33-167830.patch
Patch21: mgetty-1.1.33-turn.patch
Patch22: mgetty-1.1.33-time_range.patch
Patch23: mgetty-1.1.36-handle_spaces.patch

License: GPLv2+
Group: Applications/Communications
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires: libX11-devel, libXext-devel, texinfo-tex, texlive-dvips
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: mktemp
Requires: /usr/sbin/sendmail
URL: http://mgetty.greenie.net/

%package sendfax
Summary: Provides support for sending faxes over a modem
Requires: mgetty = %{version}
Group: Applications/Communications
Requires: mktemp
Requires: netpbm-progs
Requires(pre): /usr/sbin/useradd

%package voice
Summary: A program for using your modem and mgetty as an answering machine
Requires: mgetty = %{version}
Group: Applications/Communications

%package viewfax
Summary: An X Window System fax viewer
Group: Applications/Communications

%description
The mgetty package contains a "smart" getty which allows logins over a
serial line (i.e., through a modem). If you're using a Class 2 or 2.0
modem, mgetty can receive faxes. If you also need to send faxes,
you'll need to install the sendfax program.

If you'll be dialing in to your system using a modem, you should
install the mgetty package. If you'd like to send faxes using mgetty
and your modem, you'll need to install the mgetty-sendfax program. If
you need a viewer for faxes, you'll also need to install the
mgetty-viewfax package.

%description sendfax
Sendfax is a standalone backend program for sending fax files. The
mgetty program (a getty replacement for handling logins over a serial
line) plus sendfax will allow you to send faxes through a Class 2
modem.

If you'd like to send faxes over a Class 2 modem, you'll need to
install the mgetty-sendfax and the mgetty packages.

%description voice
The mgetty-voice package contains the vgetty system, which enables
mgetty and your modem to support voice capabilities. In simple terms,
vgetty lets your modem act as an answering machine. How well the
system will work depends upon your modem, which may or may not be able
to handle this kind of implementation.

Install mgetty-voice along with mgetty if you'd like to try having
your modem act as an answering machine.

%description viewfax
Viewfax displays the fax files received using mgetty in an X11 window.
Viewfax is capable of zooming in and out on the displayed fax.

If you're installing the mgetty-viewfax package, you'll also need to
install mgetty.

%prep
%setup -q
mv policy.h-dist policy.h
%patch0 -p1 -b .config
%patch1 -p1 -b .policy
%patch4 -p1 -b .voiceconfig
%patch5 -p1 -b .issue
%patch6 -p1 -b .issue-doc
%patch7 -p1 -b .helper
%patch8 -p1 -b .mktemp
%patch9 -p1 -b .unioninit
%patch11 -p1 -b .helper2
%patch12 -p1 -b .no-acroread
%patch14 -p1 -b .sendmail_path
%patch15 -p1 -b .lfs
%patch16 -p1 -b .162174_tcflush
%patch18 -p1 -b .bug_63843
%patch19 -p1 -b .167830_tty_access
%patch20 -p1 -b .167830
%patch21 -p1 -b .turn
%patch22 -p1 -b .time_range
%patch23 -p1 -b .handle_spaces

%build
%define makeflags CFLAGS="$RPM_OPT_FLAGS -Wall -DAUTO_PPP -D_FILE_OFFSET_BITS=64 -fno-strict-aliasing" prefix=%{_prefix} spool=%{_var}/spool BINDIR=%{_bindir} SBINDIR=%{_sbindir} LIBDIR=%{_libdir}/mgetty+sendfax HELPDIR=%{_libdir}/mgetty+sendfax CONFDIR=%{_sysconfdir}/mgetty+sendfax MANDIR=%{_mandir} MAN1DIR=%{_mandir}/man1 MAN4DIR=%{_mandir}/man4 MAN5DIR=%{_mandir}/man5 MAN8DIR=%{_mandir}/man8 INFODIR=%{_infodir} ECHO='"echo -e"' INSTALL=%{__install}
make %{makeflags}
make -C voice %{makeflags}
make -C tools %{makeflags}

pushd frontends/X11/viewfax
make OPT="$RPM_OPT_FLAGS" CONFDIR=%{_sysconfdir}/mgetty+sendfax
popd

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_infodir},%{_libdir}/mgetty+sendfax}
mkdir -p $RPM_BUILD_ROOT{%{_mandir},%{_sbindir},/sbin,/var/spool}

%define instflags CFLAGS="$RPM_OPT_FLAGS -Wall -DAUTO_PPP" prefix=$RPM_BUILD_ROOT%{_prefix} spool=$RPM_BUILD_ROOT%{_var}/spool BINDIR=$RPM_BUILD_ROOT%{_bindir} SBINDIR=$RPM_BUILD_ROOT%{_sbindir} LIBDIR=$RPM_BUILD_ROOT%{_libdir}/mgetty+sendfax HELPDIR=$RPM_BUILD_ROOT%{_libdir}/mgetty+sendfax CONFDIR=$RPM_BUILD_ROOT%{_sysconfdir}/mgetty+sendfax MANDIR=$RPM_BUILD_ROOT%{_mandir} MAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 MAN4DIR=$RPM_BUILD_ROOT%{_mandir}/man4 MAN5DIR=$RPM_BUILD_ROOT%{_mandir}/man5 MAN8DIR=$RPM_BUILD_ROOT%{_mandir}/man8 INFODIR=$RPM_BUILD_ROOT%{_infodir} ECHO='echo -e' INSTALL=%{__install}

make install %instflags
# the non-standard executable permissions are used due to security
install -m700 callback/callback $RPM_BUILD_ROOT%{_sbindir}
# helper tests internally usage of suid - this is an intention
install -m4711 callback/ct $RPM_BUILD_ROOT%{_bindir}

mv $RPM_BUILD_ROOT%{_sbindir}/mgetty $RPM_BUILD_ROOT/sbin

# this conflicts with efax
mv $RPM_BUILD_ROOT%{_mandir}/man1/fax.1 $RPM_BUILD_ROOT%{_mandir}/man1/mgetty_fax.1

# tools
make -C tools install %instflags

# voice mail extensions
mkdir -p $RPM_BUILD_ROOT%{_var}/spool/voice/{messages,incoming}
make -C voice install %instflags
mv $RPM_BUILD_ROOT%{_sbindir}/vgetty $RPM_BUILD_ROOT/sbin
# the non-standard permissions are used due to security
install -m 600 -c voice/voice.conf-dist $RPM_BUILD_ROOT%{_sysconfdir}/mgetty+sendfax/voice.conf

# don't ship documentation that is executable...
find samples -type f -exec chmod 644 {} \;

make -C frontends/X11/viewfax install %instflags MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1

# install logrotate control files
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/mgetty
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/sendfax
install -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/vgetty
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/vm

# remove file droppings from $RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_bindir}/cutbl

# remove file conflict with netpbm:
rm -f $RPM_BUILD_ROOT%{_bindir}/g3topbm

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_infodir}/mgetty.inf* ]; then
	/sbin/install-info %{_infodir}/mgetty.info.gz %{_infodir}/dir --entry="* mgetty: (mgetty).		Package to handle faxes, voicemail and more." || :
fi

%preun
if [ -f %{_infodir}/mgetty.inf* ]; then
    /sbin/install-info --delete %{_infodir}/mgetty.info.gz %{_infodir}/dir --entry="* mgetty: (mgetty). 	Package to handle faxes, voicemail and more." || :
fi

%pre sendfax
getent group fax >/dev/null || groupadd -g %SENDFAX_UID -r fax
getent passwd fax >/dev/null || \
  useradd -r -u %SENDFAX_UID -g fax -d /var/spool/fax -s /sbin/nologin -c "mgetty fax spool user" fax
exit 0

%files
%defattr(-,root,root)
%doc BUGS ChangeLog README.1st Recommend THANKS doc/modems.db samples
%doc doc/mgetty.ps doc/*.txt
%{_bindir}/g3cat
%{_bindir}/g32pbm
/sbin/mgetty
%{_sbindir}/callback
%{_mandir}/man1/g32pbm.1*
%{_mandir}/man1/g3cat.1*
%{_mandir}/man4/mgettydefs.4*
%{_mandir}/man8/mgetty.8*
%{_mandir}/man8/callback.8*
%{_infodir}/mgetty.info*
%dir %{_sysconfdir}/mgetty+sendfax
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/login.config
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/mgetty.config
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/dialin.config
%config(noreplace) %{_sysconfdir}/logrotate.d/mgetty

%files sendfax
%defattr(-,root,root)
%dir %{_var}/spool/fax
%attr(0755,fax,root) %dir %{_var}/spool/fax/incoming
%attr(0755,fax,root) %dir %{_var}/spool/fax/outgoing
%attr(0755,root,root) %{_bindir}/ct
%{_bindir}/faxq
%{_bindir}/faxrm
%{_bindir}/faxrunq
%{_bindir}/faxspool
%{_bindir}/kvg
%{_bindir}/newslock
%{_bindir}/pbm2g3
%{_bindir}/sff2g3
%{_sbindir}/faxrunqd
%{_sbindir}/sendfax
%dir %{_libdir}/mgetty+sendfax
%{_libdir}/mgetty+sendfax/cour25.pbm
%{_libdir}/mgetty+sendfax/cour25n.pbm
# helper tests internally usage of suid - this is an intention
%attr(04711,fax,root) %{_libdir}/mgetty+sendfax/faxq-helper
%{_mandir}/man1/pbm2g3.1*
%{_mandir}/man1/mgetty_fax.1*
%{_mandir}/man1/faxspool.1*
%{_mandir}/man1/faxrunq.1*
%{_mandir}/man1/faxq.1*
%{_mandir}/man1/faxrm.1*
%{_mandir}/man1/coverpg.1*
%{_mandir}/man1/sff2g3.1*
%{_mandir}/man5/faxqueue.5*
%{_mandir}/man8/faxq-helper.8*
%{_mandir}/man8/faxrunqd.8*
%{_mandir}/man8/sendfax.8*
%dir %{_sysconfdir}/mgetty+sendfax
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/sendfax.config
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/faxrunq.config
# sample config file doesn't use noreplace option to be installed always latest ver.
%config %{_sysconfdir}/mgetty+sendfax/faxspool.rules.sample
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/faxheader
# logrotate file name uses only sub-package name
%config(noreplace) %{_sysconfdir}/logrotate.d/sendfax

%files voice
%defattr(-,root,root)
%doc voice/doc/* voice/Announce voice/ChangeLog voice/Readme
%dir %{_var}/spool/voice
%dir %{_var}/spool/voice/incoming
%dir %{_var}/spool/voice/messages
/sbin/vgetty
%{_bindir}/vm
%{_bindir}/pvfamp
%{_bindir}/pvfcut
%{_bindir}/pvfecho
%{_bindir}/pvffft
%{_bindir}/pvffile
%{_bindir}/pvffilter
%{_bindir}/pvfmix
%{_bindir}/pvfnoise
%{_bindir}/pvfreverse
%{_bindir}/pvfsine
%{_bindir}/pvfspeed
%{_bindir}/rmdfile
%{_bindir}/pvftormd
%{_bindir}/rmdtopvf
%{_bindir}/pvftovoc
%{_bindir}/voctopvf
%{_bindir}/pvftolin
%{_bindir}/lintopvf
%{_bindir}/pvftobasic
%{_bindir}/basictopvf
%{_bindir}/pvftoau
%{_bindir}/autopvf
%{_bindir}/pvftowav
%{_bindir}/wavtopvf
%{_mandir}/man1/zplay.1*
%{_mandir}/man1/pvf.1*
%{_mandir}/man1/pvfamp.1*
%{_mandir}/man1/pvfcut.1*
%{_mandir}/man1/pvfecho.1*
%{_mandir}/man1/pvffile.1*
%{_mandir}/man1/pvffft.1*
%{_mandir}/man1/pvfmix.1*
%{_mandir}/man1/pvfreverse.1*
%{_mandir}/man1/pvfsine.1*
%{_mandir}/man1/pvfspeed.1*
%{_mandir}/man1/pvftormd.1*
%{_mandir}/man1/pvffilter.1*
%{_mandir}/man1/pvfnoise.1*
%{_mandir}/man1/rmdtopvf.1*
%{_mandir}/man1/rmdfile.1*
%{_mandir}/man1/pvftovoc.1*
%{_mandir}/man1/voctopvf.1*
%{_mandir}/man1/pvftolin.1*
%{_mandir}/man1/lintopvf.1*
%{_mandir}/man1/pvftobasic.1*
%{_mandir}/man1/basictopvf.1*
%{_mandir}/man1/pvftoau.1*
%{_mandir}/man1/autopvf.1*
%{_mandir}/man1/pvftowav.1*
%{_mandir}/man1/wavtopvf.1*
%{_mandir}/man8/vgetty.8*
%dir %{_sysconfdir}/mgetty+sendfax
%config(noreplace) %{_sysconfdir}/mgetty+sendfax/voice.conf
# logrotate file name uses only sub-package name
%config(noreplace) %{_sysconfdir}/logrotate.d/vgetty
%config(noreplace) %{_sysconfdir}/logrotate.d/vm

%files viewfax
%defattr(-,root,root)
%doc frontends/X11/viewfax/C* frontends/X11/viewfax/README
%{_bindir}/viewfax
%dir %{_libdir}/mgetty+sendfax
%{_libdir}/mgetty+sendfax/viewfax.tif
%{_mandir}/man1/viewfax.1*

%changelog
* Thu Jun 03 2010 Jiri Skala <jskala@redhat.com> - 1.1.36-8
- Resolves: #599389 - RPMdiff run failed. Added no-strict-alisting option

* Fri May 21 2010 Jiri Skala <jskala@redhat.com> - 1.1.36-7
- Resolves: #594402 - wrong users and groups creation in spec file

* Fri Jan 29 2010 Jiri Skala <jskala@redhat.com> - 1.1.36-6
- Resolves: #555835 - spec corrections noticed by rpmlint

* Mon Sep 14 2009 Jiri Skala <jskala@redhat.com> - 1.1.36-5
- fixed #516001 - Errors installing mgetty with --excludedocs

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 10 2008 Jiri Skala <jskala@redhat.com> - 1.1.36-1
- fix #464983 - FTBFS mgetty-1.1.36-1.fc10 - regenerated patches

* Thu Apr 10 2008 Martin Nagy <mnagy@redhat.com> - 1.1.36-1
- update to new upstream release
- use our own faxq-helper man page now that we updated
- fix -t flag of faxspool so it now accepts time ranges as it should (#171280)
- fix mgetty and vgetty logrotate configuration files (#436727)
- faxspool will handle spaces in file names better (#46697)

* Thu Apr 03 2008 Martin Nagy <mnagy@redhat.com> - 1.1.33-17
- make sure we compile everything with FORTIFY_SOURCE

* Wed Mar 05 2008 Martin Nagy <mnagy@redhat.com> - 1.1.33-16
- fix -t option of g32pbm (#188028)
- move g32pbm and g3cat from mgetty-sendfax to mgetty (#190179)
- some whitespace changes (#263641)
- added faxq-helper man page (#243293)

* Mon Feb 18 2008 Jindrich Novy <jnovy@redhat.com> - 1.1.33-15
- fix BuildRoot, License tag
- fix policy and issue patches
- remove useless rpm macros
- rpmlint fixes

* Sat Feb 17 2008 Jindrich Novy <jnovy@redhat.com> - 1.1.33-14
- fix broken BuildRequires (#433177)

* Mon Jan 28 2008 Martin Nagy <mnagy@redhat.com> - 1.1.33-13
- fix homepage URL (#353531)
- correct Requires

* Wed Jan 09 2008 Martin Nagy <mnagy@redhat.com> - 1.1.33-12
- changed MAILER from /usr/lib/sendmail to /usr/sbin/sendmail (#427585)

* Thu Sep 06 2007 Maros Barabas <mbarabas@redhat.com> - 1.1.33-11
- rebuild

* Tue Jan 23 2007 Maros Barabas <mbarabas@redhat.com> - 1.1.33-10
- fixed install-info scriptlets (post,preun)
- Resolves #223710

* Mon Aug 21 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.1.33-9
- add /usr/sbin/useradd as a prereq for the -sendfax subpackage, because
  we call it during the -sendfax %%pre scriptlet (#203266)

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 1.1.33-8
- Change BuildPrereq from texinfo to texinfo-tex

* Mon Mar 27 2006 Miloslav Trmac <mitr@redhat.com> - 1.1.33-7.FC5.3
- Change BuildPrereq from texinfo to texinfo-tex

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1.33-7.FC5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1.33-7.FC5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Dec 18 2005 Jason Vas Dias<jvdias@redhat.com> - 1.1.33-7.FC5
- rebuild for new gcc + remove 'xmkmf' invocation for Modular X11

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug 01 2005 Jason Vas Dias <jvdias@redhat.com> 1.1.33-4_FC5
- fix bug 63848

* Fri Jul 22 2005 Jason Vas Dias <jvdias@redhat.com> 1.1.33-3_FC5
- fix bug 162174: prevent uninterruptable hang on exit() when
                  direct line disconnected (kernel bug 164002)
                  do tcflush(1,TCOFLUSH) before exit() in sig_goodbye()
                  block signals before entering syslog()
  workaround build system 'buffer overflow checks' bug:
                  use memcpy instead of sprintf in record.c, line 53

* Mon Apr 25 2005 Jason Vas Dias <jvdias@redhat.com> 1.1.33-1
- Upgrade to new upstream version 1.1.33

* Thu Apr 21 2005 Peter Vrabec <pvrabec@redhat.com> 1.1.31-5
- support FILE_OFFSET_BITS=64 in statvfs (#155440)

* Wed Mar 16 2005 Jason Vas Dias <jvdias@redhat.com> 1.1.31-4
- Rebuild for gcc4

* Mon Feb 21 2005 Jason Vas Dias <jvdias@redhat.com> 1.1.31-3
- fix bug 145582: wrong path to sendmail
- Rebuild for FC4

* Fri Aug 20 2004 Jason Vas Dias <jvdias@redhat.com> 1.1.31-2
- Fixed bug: 115164 - remove *printf format errors

* Fri Aug 20 2004 Jason Vas Dias <jvdias@redhat.com> 1.1.31-2
- Fixed bug: 115261 - let faxspool work if acroread isn't installed
- or gs can't understand its level3 output .

* Tue Aug 17 2004 Jason Vas Dias <jvdias@redhat.com> 1.1.31-1
- Upgraded to 1.1.31

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 18 2004 Jeremy Katz <katzj@redhat.com> 1.1.30-8
- rebuild

* Tue May 18 2004 Nalin Dahyabhai <nalin@redhat.com> 1.1.30-7
- mark configuration files config(noreplace) (#123439)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Nov 18 2003 Nalin Dahyabhai <nalin@redhat.com> 1.1.30-5
- fix paths given for faxq-helper in faxq and faxrm (#92090)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May  1 2003 Elliot Lee <sopwith@redhat.com> 1.1.30-3
- ppc64 calls for the union init patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 19 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.30-1
- update to 1.1.30
- use mktemp to make the temporary file when spooling fax data from stdin

* Tue Dec 10 2002 Elliot Lee <sopwith@redhat.com> 1.1.29-1
- Fix logrotate.vgetty wildcard

* Mon Nov 25 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.29-1
- update to 1.1.29
- create the fax user in -sendfax %%pre
- remove /var/spool/fax/outgoing/locks

* Tue Nov 12 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.28-10
- define PTR_IS_LONG on x86_64

* Tue Nov 12 2002 Tim Powers <timp@redhat.com>
- remove files from $RPM_BUILD_ROOT that we aren't including

* Tue Sep  3 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.28-9
- include vgetty's man page

* Fri Aug 23 2002 Elliot Lee <sopwith@redhat.com> 1.1.28-8
- /var/spool/fax/outgoing/locks needs to be sticky

* Tue Aug 13 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.28-7
- rotate mgetty.log.unknown and mgetty.log.callback (#68049)
- don't logrotate already-rotated logs (#68422)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.28-4
- rebuild in new environment

* Thu Feb 28 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.28-3
- rotate the mgetty and vgetty logs by default, specifying them with
  wildcards in the logrotate configs (#62159)

* Fri Feb 22 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.28-2
- rebuild

* Fri Jan 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.28-1
- update to 1.1.28

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Oct 22 2001 Nalin Dahyabhai <nalin@redhat.com> 1.1.27-1
- update to 1.1.27
- drop s390x patch (no longer needed)

* Tue Jul 24 2001 Nalin Dahyabhai <nalin@redhat.com> 1.1.26-6
- tweak the issue patch

* Tue Jul 10 2001 Bill Nottingham <notting@redhat.com>
- make /etc/issue parsing match other gettys

* Tue Jun 12 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add 64 bit patch for s390x from <oliver.paukstadt@millenux.com>

* Wed Apr 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- define _sysconfdir, not sysconfdir

* Mon Apr 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.1.26
- add logrotate.vm and logrotate.vgetty (note from Heiner Kordewiner)
- add voice/{Announce,Changelog,Readme} to documentation set

* Tue Apr 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- define CNDFILE in policy.h

* Tue Mar 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- change the default group in the vgetty configuration file from phone to uucp,
  which matches the settings for faxes

* Tue Mar 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.1.25
- ditch the elsa patch in favor of the current vgetty patch
- don't need to strip binaries, buildroot policies do that
- add docs to the voice subpackage

* Tue Jan 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- use mkdtemp() when printing faxes

* Mon Jan 15 2001 Preston Brown <pbrown@redhat.com>
- fix misdetection of USR voice modem detection <cjj@u.washington.edu>

* Mon Jan 08 2001 Preston Brown <pbrown@redhat.com>
- 1.1.24 includes tmpfile security enhancements, some of our patches

* Tue Sep 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- back out quoting patch
- change Copyright: distributable to License: GPL
- add URL
- remove logging changes from excl patch, based on input from Gert
- rework ia64 patch, break out gets/fgets change based on input from Gert

* Thu Sep  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- make sure all scripts quote variables where possible (#17179)
- make sure all scripts use mktemp for generating temporary files

* Sat Aug 26 2000 Bill Nottingham <notting@redhat.com>
- update to 1.1.22; fixes security issues

* Mon Aug  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix excl patch to keep everything from segfaulting all the time (#11523,11590)

* Mon Jul 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- forcibly strip binaries (#12431)
- change dependency on libgr-progs (which is gone) to netgr-progs (#10819)
- change dependency on giftoppm to giftopnm (#8088)
- attempt to plug some potential security problems (#11874)

* Thu Jul 12 2000 Than Ngo <than@redhat.de>
- add new V250modem patch from ELSA (thanks to Jürgen Kosel)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 23 2000 Than Ngo <than@redhat.de>
- add support ELSA Microlink 56k

* Sun Jun  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- Overhaul for FHS fixes.
- Stop removing logs in postun.
- Stop stripping everything.
- ia64 fixes.

* Wed May 17 2000 Ngo Than <than@redhat.de>
- updated the new vgetty (#bug 10440)

* Sat May  6 2000 Bill Nottingham <notting@redhat.com>
- fix compilation with new gcc, or ia64, or something...

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed

* Tue Sep  7 1999 Jeff Johnson <jbj@redhat.com>
- add fax print command (David Fox).

* Tue Sep 07 1999 Cristian Gafton <gafton@redhat.com>
- version 1.1.21

* Tue Aug 31 1999 Jeff Johnson <jbj@redhat.com>
- move callback to base package (#4799).

* Wed Jun  2 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.1.20 (#3216).

* Tue Apr  6 1999 Bill Nottingham <notting@redhat.com>
- strip setuid bit from ct

* Tue Mar 23 1999 Preston Brown <pbrown@redhat.com>
- better log handling

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- rebuild for glibc 2.1

* Sat Aug 22 1998 Jos Vos <jos@xos.nl>
- Use a patch for creating policy.h using policy.h-dist.
- Add viewfax subpackage (X11 fax viewing program).
- Add logrotate config files for mgetty and sendfax log files.
- Properly define ECHO in Makefile for use with bash.
- Add optional use of dialin.config (for modems supporting this).
- Change default notification address to "root" (was "faxadmin").
- Change log file names according to better defaults.
- Change default notify program to /etc/mgetty+sendfax/new_fax (was
  /usr/local/bin/new_fax).

* Fri Aug 21 1998 Jeff Johnson <jbj@redhat.com>
- add faxrunqd man page (problem #850)
- add missing pbm2g3 (and man page); remove unnecessary "rm -f pbmtog3"
- delete redundant ( cd tools; make ... )

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.1.14
- AutoPPP patch

* Thu Dec 18 1997 Mike Wangsmo <wanger@redhat.com>
- added more of the documentation files to the rpm

* Wed Oct 29 1997 Otto Hammersmith <otto@redhat.com>
- added install-info support

* Tue Oct 21 1997 Otto Hammersmith <otto@redhat.com>
- updated version

* Wed Oct 15 1997 Erik Troan <ewt@redhat.com>
- now requires libgr-progs instead of netpbm

* Mon Aug 25 1997 Erik Troan <ewt@redhat.com>
- built against glibc
