/* $Id$ */

#ifndef EL__DOTDOT_FEATURE_H
#define EL__DOTDOT_FEATURE_H

/* This file contains various compile-time configuration settings, which you
 * can adjust below. You can fine-tune the ELinks binary to include really only
 * what you want it to. There are still some things which are to be adjusted
 * only directly through the ./configure script arguments though, so check
 * ./configure --help out as well! */

/* For users:
 *
 * The "/" "*" and "*" "/" sequences start/end comments in this file. The
 * features are controlled by using the "#define FEATURE" command. If it is
 * commented out, it means the feature is disabled, otherwise it is enabled.
 * Therefore, if the default doesn't suit you, you can either comment it out
 * or remove the comment marks. */

/* For developers:
 *
 * Please strive to keep the format of all entries uniform, it will make it
 * easier for us as well as for the users. Do not forget to accurately describe
 * the feature and also the impact of enabling/disabling it. Follow the format
 * of existing comments. Follow the example of XBEL when adding features which
 * also need some detection in configure.in.
 *
 * Not everything is suitable for an entry in this file, maybe it would be
 * happier directly in the configure.in. Basically, if it is going to have the
 * commandline argument in ./configure anyway (the M4 macro expansion does it,
 * like --with-x or --without-nls), do not add it here. If it is really purely
 * question of system support (X2, HAVE_SA_STORAGE), and it makes no sense for
 * the user to touch it, do not include it here.
 *
 * Also, use your common sense. (Not that I would trust it that much... ;-))
 * --pasky */



/*** LEDs
 *
 * These are the tiny LED-like indicators, shown at the bottom-right of the
 * screen as [-----]. They are used for indication of various states, ie.
 * whether you are currently talking through a SSL-secured connection.
 *
 * This is rather a fancy thing, and it doesn't do anything actually useful yet
 * anyway.
 *
 * Default: disabled */

/* #define CONFIG_LEDS */


/*** Bookmarks
 *
 * ELinks has built-in hiearchic bookmarks support. Open the bookmarks manager
 * by pressing 's'. When bookmarks are enabled, also support for the internal
 * ELinks bookmarks format is always compiled in.
 *
 * This is a favourite target for disabling in various embedded applications.
 * It all depends on your requirements.
 *
 * Default: enabled */

#define CONFIG_BOOKMARKS


/*** XBEL Bookmarks
 *
 * ELinks also supports universal XML bookmarks format called XBEL, also
 * supported by ie. Galeon, various "always-have-my-bookmarks" websites and
 * number of universal bookmark convertors.
 *
 * Frequently, you know you will not need it, then you can of course happily
 * forcibly remove support for it and save few bytes.
 *
 * Default: enabled if libexpat (required library) found and bookmarks are
 * enabled */

#if defined(HAVE_LIBEXPAT) && defined(CONFIG_BOOKMARKS)
/* Comment out the following line if you want to always have this disabled: */
#define CONFIG_XBEL_BOOKMARKS
#endif


/*** Cookies
 *
 * Support for HTTP cookies --- a data token which the server sends the client
 * once and then the client sends it back along each request to the server.
 * This mechanism is crucial for ie. keeping HTTP sessions (you "log in" to a
 * site, and from then on the site recognizes you usually because of the
 * cookie), but also for various banner systems, remembering values filled to
 * various forms, and so on. You can further tune the ELinks behaviour at
 * runtime (whether to accept/send cookies, ask for confirmation when accepting
 * a cookie etc).
 *
 * This functionality is usually quite important and you should not disable it
 * unless you really know what are you doing.
 *
 * Default: enabled */

#define CONFIG_COOKIES


/*** Global History
 *
 * This device records each and every page you visit (to a configurable limit).
 * You can browse through this history in the history manager (press 'h').  Do
 * not confuse this with the "session history", recording history of your
 * browsing in the frame of one session (session history is the thing you move
 * through when pressing 'back' and 'unback' or which you see in the
 * File::History menu).
 *
 * Global history does not care about the order you visited the pages in, it
 * just records that you visited it, when did you do that and the title of the
 * page. Then, you can see when did you visit a link last time (and what was
 * the title of the target document at that time), links can be coloured as
 * visited etc.
 *
 * If you disable this feature, you will not lose any crucial functionality,
 * just some relatively minor convenience features, which can nevertheless
 * prove sometimes very practical.
 *
 * Default: enabled */

#define CONFIG_GLOBHIST



/*** URI Rewriting
 *
 * The goto dialog through which new URIs can be entered is an essential part
 * of browsing in ELinks. This feature makes the dialog more powerful by making
 * it possible to extend how entered text is handled through a set of rewrite
 * rules (see protocol.rewrite options).
 *
 * There are two types of rules: simple and smart ones.
 *
 * Simple rewriting rules are basicly URI abbreviations, making it possible to
 * map a word to the full URI. They can also be used for hierarchic navigation
 * to ease moving from some nested directory to the parent directory or doing
 * other stuff with the current URI. For example, when you type 'gg' into the
 * goto dialog, you will be materialized at Google's homepage.
 *
 * Smart rules can take arguments and therefore enable more advanced rewriting.
 * The arguments could be search words to google for or a lookup query for a
 * dictionary. Eg. type 'gg:Petr Baudis king of ELinks cvs'.
 *
 * This feature is also available in a more powerful form in the Lua and Guile
 * extensions, so if you plan to or already use those, you won't miss anything
 * by disabling this feature (besides easier and better integrated
 * configuration).
 *
 * Default: enabled */

#define CONFIG_URI_REWRITE



/*** MIME
 *
 * ELinks uses a MIME system for determining the content type of documents and
 * configuring programs for external handling. By default the option system can
 * be used to configure how media types are handled. More info about how to set
 * up the MIME handling using the option system can be found in the
 * doc/mime.html file.
 *
 * Below are listed some additional ways to do it. */

/*** Mailcap
 *
 * Mailcap files describe what program - on the local system - can be used to
 * handle a media type. The file format is defined in RFC 1524 and more info
 * including examples can be found in the doc/mailcap.html file.
 *
 * This is very useful especially for clean interoperability with other
 * MIME-aware applications and fitting nicely into the UNIX system, where this
 * is the standard way of specifying MIME handlers. If you are not interested
 * in that, you can still use the internal MIME associations system, though.
 *
 * Default: enabled */

#define CONFIG_MAILCAP

/*** Mimetypes File
 *
 * Mimetypes file can be used to specify the relation between media types and
 * file extensions.
 *
 * Basically same thing applies here as for the mailcap support.
 *
 * Default: enabled */

#define CONFIG_MIMETYPES



/*** 256 Colors in Terminals
 *
 * Define to add support for using 256 colors in terminals. Note that this
 * requires a capable terminal emulator, such as:
 *
 * - Thomas Dickey's XTerm, version 111 or later (check which version you have
 *   with xterm -version) compiled with --enable-256-color.
 *
 * - Recent versions of PuTTY also have some support for 256 colors.
 *
 * You will still need to enable this at runtime for a given terminal in
 * terminal options, or set your $TERM variable to xterm-256color - then,
 * ELinks will automatically configure itself to make use of all the available
 * terminal features, while still acting sensibly when you happen to run it in
 * an xterm w/o the 256 colors support.
 *
 * When enabled, the memory usage is somewhat increased even when running in
 * mono and 16 colors mode (the memory consumption can be especially remarkable
 * when rendering very large documents and/or using very large terminals).
 * However, when you actually run it in the suitable terminal, it looks really
 * impressive, I'd say marvelous!
 *
 * Default: disabled */

/* #define CONFIG_256_COLORS */


/*** Backtrace Printing
 *
 * Once upon a time, a disaster happens and ELinks crashes. That is a very sad
 * event and it would be very nice to have some means how to diagnose it. In
 * the crash handler, ELinks prints out various helpful things, however the
 * truly important information is _where_ did it crash. Usually, users do not
 * have gdb installed and can't provide a backtrace. However, ELinks can print
 * a backtrace on its own, if the system supports it (currently, it is
 * implemented only for glibc). It is not always accurate, it is useless when
 * the ELinks binary is stripped and it still misses a lot of important
 * information, but it can be sometimes still an indispensable help for the
 * developers.
 *
 * You should keep this, unless you will strip your ELinks binary anyway, you
 * know you are not going to report back any failures and you care about each
 * single wasted bit.
 *
 * Default: enabled if the libc supports it (only glibc) */

#ifdef CONFIG_BACKTRACE
/* Uncomment the following line if you want to always have this disabled: */
/* #undef CONFIG_BACKTRACE */
#endif


/*** Disable Root User
 *
 * Browsers are scary monsters used for traveling around in an even more scary
 * world where people indifferently throw garbage files at you and threaten
 * your perfect world. Altho' ELinks is a small monster compared to most
 * browsers, it can still bite your head off and some might consider running it
 * as the root user extremely dangerous. To prevent such usage simply enable
 * this feature.
 *
 * Default: disabled */

#if defined(HAVE_GETUID) && defined(HAVE_GETEUID)
/* Uncomment the following line if you want to enable this: */
/* #define CONFIG_NO_ROOT_EXEC */
#endif


/*** Form History
 *
 * The famous Competing Browser has that annoying thing which pops up when you
 * submit a form, offering to remember it and pre-fill it the next time. And
 * yes, ELinks can do that too! You will still need to also enable this manualy
 * at document.browse.forms.show_formhist.
 *
 * Many people find it extremely annoying (including pasky), however some
 * others consider it extremely handy and will sacrifice almost anything to get
 * it. It will not do any harm to have this compiled-in as long as you will
 * leave it turned off (which is also the default configuration).
 *
 * Default: enabled */

#define CONFIG_FORMHIST


/*** Mouse Support
 *
 * ELinks may be controlled not only by keyboard, but also by mouse to quite
 * some extent. You can select links, menu items, scroll document, click at
 * buttons etc, and it should hopefully work. ELinks supports mouse control by
 * GPM, xterm mouse reporting and TWAIN's twterm mouse reporting.
 *
 * It is generally nice convience and doesn't cost too much. However, you can
 * do everything with keyboard as you can with mouse. Also note that the xterm
 * mouse reporting takes control over the terminal so that copy and pasting
 * text from and to ELinks has to be done by holding down the Shift key.
 *
 * Default: enabled */

#define CONFIG_MOUSE


/*** Local CGI Support
 *
 * ELinks can (like w3m or lynx) execute certain executable files stored on the
 * local disks as CGIs, when you target it on them (through a URI of the 'file'
 * scheme). ELinks emulates the complete CGI environment, like the program
 * would be executed by a web server. See the protocol.file.cgi options tree
 * for detailed runtime configuration.
 *
 * Some people just write their bookmark managment application as perl CGI
 * script and then access it from the web browser using this feature, not
 * needing any web server or so. Therefore, this is a great possible way to
 * extended the browser capabilities.
 *
 * Even when you compile this in, you need to enable this yet in the
 * configuration, and even then only CGI files passing certain user-defined
 * filters (path-based) will be allowed to be executed (and there are certain
 * other security barriers in place).
 *
 * Default: disabled */

#ifdef HAVE_SETENV
/* Uncomment the following line if you want to enable this: */
/* #define CONFIG_CGI */
#endif


/*** SMB Protocol Support
 *
 * ELinks supports browsing over the SMB protocol (URI 'smb' scheme), using the
 * smbclient program as backend. Therefore, in order to have this enabled, you
 * will need to install Samba (or at least just the smbclient part, if you can
 * install it separately).
 *
 * Default: enabled if smbclient will be found */

#ifdef CONFIG_SMB
/* Uncomment the following line if you want to always have this disabled: */
/* #undef CONFIG_SMB */
#endif


#endif
