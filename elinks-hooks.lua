-- Example hooks.lua file, put in ~/.links/ as hooks.lua.
-- $Id$


----------------------------------------------------------------------
--  Local configuration
----------------------------------------------------------------------

-- ** IMPORTANT **
-- For security reasons, systems functions are not enabled by default.
-- To do so, uncomment the following line, but be careful about
-- including unknown code.  Individual functions may be disabled by
-- assigning them to `nil'.

     enable_systems_functions ()

    -- openfile = nil    -- may open files in write mode
    -- readfrom = nil    -- reading from pipe can execute commands
    -- writeto = nil
    -- appendto = nil
    -- pipe_read = nil
    -- remove = nil
    -- rename = nil
    -- execute = nil
    -- exit = nil

-- Home directory: If you do not enable system functions, you will
-- need to set the following to your home directory.

    home_dir = (getenv and getenv ("HOME")) or "/home/MYSELF"
    hooks_file = home_dir.."/.links/hooks.lua"

-- Pausing: When external programs are run, sometimes we need to pause
-- to see the output.  This is the string we append to the command
-- line to do that.  You may customise it if you wish.

    pause = '; echo -ne "\\n\\e[1;32mPress ENTER to continue...\\e[0m"; read'

-- When starting Netscape: Set to `nil' if you do not want to open a
-- new window for each document.

    netscape_new_window = 1

-- Make ALT="" into ALT="&nbsp;": Makes web pages with superfluous
-- images look better.  However, even if you disable the "Display links
-- to images" option, single space links to such images will appear.
-- To enable, set the following to 1.  If necessary, you can change
-- this while in Links using the Lua Console, then reload the page.
-- See also the keybinding section at the end of the file.

    mangle_blank_alt = nil

-- WWWoffle is a proxy/cache system designed for dial-up users.
-- If you have it, set this to the machine:port where it is installed 
-- (e.g. "http://localhost:8080")

    wwwoffle = nil

-- If you set this to non-`nil', the bookmark addon will be loaded,
-- and actions will be bound to my key bindings.  Change them at the
-- bottom of the file.

    bookmark_addon = nil


----------------------------------------------------------------------
--  case-insensitive gsub
----------------------------------------------------------------------

-- Please note that this is not completely correct yet.
-- It will not handle pattern classes like %a properly.
-- XXX: Fix this to handle pattern classes.

function gisub (s, pat, repl, n)
    pat = gsub (pat, '(%a)', 
	        function (v) return '['..strupper(v)..strlower(v)..']' end)
    if n then
	return gsub (s, pat, repl, n)
    else
	return gsub (s, pat, repl)
    end
end


----------------------------------------------------------------------
--  goto_url_hook
----------------------------------------------------------------------

function match (prefix, url)
    return strsub (url, 1, strlen (prefix)) == prefix
end

function strip (str)
    return gsub (str, "^%s*(.-)%s*$", "%1")
end

function plusify (str)
    return gsub (str, "%s", "+")
end

function goto_url_hook (url, current_url)

    -- XXX: Use a table instead of if ... else ... else ...

    -- Google search (e.g. ,gg unix browsers).
    if match (",gg", url) then
        url = plusify (strip (strsub (url, 4)))
        return "http://www.google.com/search?q="..url.."&btnG=Google+Search"
 
    -- Freshmeat search.
    elseif match (",fm", url) then
        url = plusify (strip (strsub (url, 4)))
        return "http://www.freshmeat.net/search/?q="..url

    -- Appwatch search (e.g. ,aw lynx).
    elseif match (",aw", url) then
        url = plusify (strip (strsub (url, 4)))
        return "http://www.appwatch.com/Linux/Users/find?q="..url

    -- Dictionary.com search (e.g. ,dict congenial).
    elseif match (",dict", url) then
        url = plusify (strip (strsub (url, 6)))
        return "http://www.dictionary.com/cgi-bin/dict.pl?db=%2A&term="..url

    -- RPM search (e.g. ,rpm links).
    elseif match (",rpm", url) then
        url = plusify (strip (strsub (url, 5)))
        return "http://www.rpmfind.net/linux/rpm2html/search.php?query="
                ..url.."&submit=Search+..."

    -- Netcraft.com search (e.g. ,whatis www.google.com).
    elseif match (",whatis", url) then
        url = plusify (strip (strsub (url, 8)))
        return "http://uptime.netcraft.com/up/graph/?host="..url

    -- LinuxToday home page.
    elseif match (",lt", url) then
        return "http://linuxtoday.com/"

    -- User Friendly daily static.
    elseif match (",uf", url) then
	return "http://www.userfriendly.org/static/"

    -- Weather forecast for Melbourne, Australia.
    elseif match (",forecast", url) then
        return "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDF02V00.txt"

    -- Local network web server.
    elseif match (",local", url) then
	return "http://desky/"

    -- WWWoffle caches.
    elseif match (",cache", url) and wwwoffle then
	return wwwoffle.."/#indexes"
 
    -- Expand ~ to home directories.
    elseif match ("~", url) then
        if strsub(url, 2, 2) == "/" then    -- ~/foo
            return home_dir..strsub(url, 2)
        else                                -- ~foo/bar
            return "/home/"..strsub(url, 2)
        end

    -- Unmatched.
    else
        return url
    end
end


-----------------------------------------------------------------------
--  follow_url_hook
---------------------------------------------------------------------

function follow_url_hook (url)
    -- Using bookmark addon.
    if bookmark_addon then
	if bm_is_category (url) then
	    return nil
	else
	    return bm_get_bookmark_url (url) or url
	end

    -- Not using bookmark addon.
    else
	return url
    end
end


----------------------------------------------------------------------
--  pre_format_html_hook
----------------------------------------------------------------------

-- Plain strfind (no metacharacters).
function sstrfind (s, pattern)
    return strfind (s, pattern, 1, 1)
end

function pre_format_html_hook (url, html)
    local ret = nil

    -- Handle gzip'd files within reasonable size.
    if strfind (url, "%.gz$") and strlen (html) < 65536 then
        local tmp = tmpname ()
        writeto (tmp) write (html) writeto ()
        html = pipe_read ("(gzip -dc "..tmp.." || cat "..tmp..") 2>/dev/null")
        remove (tmp)
        ret = 1
    end

    -- Mangle ALT="" in IMG tags.
    if mangle_blank_alt then
	local n
	html, n = gisub (html, '(<img.-) alt=""', '%1 alt="&nbsp;"')
	ret = ret or (n > 0)
    end

    -- These quick 'n dirty patterns don't maintain proper HTML.

    -- linuxtoday.com
    if sstrfind (url, "linuxtoday.com") then
        if sstrfind (url, "news_story") then
            html = gsub (html, '<TABLE CELLSPACING="0".-</TABLE>', '', 1)
            html = gsub (html, '<TR BGCOLOR="#FFF.-</TR></TABLE>', '', 1)
        else
            html = gsub (html, 'WIDTH="120">\n<TR.+</TABLE></TD>', '>', 1)
        end
        html = gsub (html, '<A HREF="http://www.internet.com.-</A>', '')
        html = gsub (html, "<IFRAME.-</IFRAME>", "")
        -- emphasis in text is lost
        return gsub (html, 'text="#002244"', 'text="#001133"', 1)

    -- linuxgames.com
    elseif sstrfind (url, "linuxgames.com") then
        return gsub (html, "<CENTER>.-</center>", "", 1)

    -- dictionary.com
    elseif sstrfind (url, "dictionary.com/cgi-bin/dict.pl") then
	local t = { t = "" }
	local _, n = gsub (html, "resultItemStart %-%-%>(.-)%<%!%-%- resultItemEnd",
			   function (x) %t.t = %t.t.."<tr><td>"..x.."</td></tr>" end)
	if n == 0 then
	    -- we've already mangled this page before
	    return html
	else
	    return "<html><head><title>Dictionary.com lookup</title></head>"..
		    "<body><table border=1 cellpadding=5>"..t.t.."</table>"..
		    "</body></html>"
	end
    end

    return ret and html
end


----------------------------------------------------------------------
--  Miscellaneous functions, accessed with the Lua Console.
----------------------------------------------------------------------

-- Reload this file (hooks.lua) from within Links.
function reload ()
    dofile (hooks_file)
end

-- Helper function.
function catto (output)
    local doc = current_document_formatted (79)
    if doc then writeto (output) write (doc) writeto () end
end

-- Print the current document using `lpr'.
function lpr ()
    -- You must compile Lua with `popen' support for pipes to work.
    -- See `config' in the Lua distribution.
    catto ("|lpr")
end

-- Print the current document using `enscript'.
function enscript ()
    catto ("|enscript -fCourier8")
end

-- Ask WWWoffle to monitor the current page for us.
-- This only works when called from lua_console_hook, below.
function monitor ()
    if wwwoffle then
	return "goto_url", wwwoffle.."/monitor-options/?"..current_url ()
    else
	return nil
    end
end

-- Email the current document, using Mutt (http://www.mutt.org).
-- This only works when called from lua_console_hook, below.
function mutt ()
    local tmp = tmpname ()
    writeto (tmp) write (current_document ()) writeto ()
    tinsert (tmp_files, tmp)
    return "run", "mutt -a "..tmp
end

-- Open current document in Netscape.
function netscape ()
    local new = netscape_new_window and ",new_window" or ""
    execute ("( netscape -remote 'openURL("..current_url ()..new..")'"
             .." || netscape '"..current_url ().."' ) 2>/dev/null &")
end

-- If Links is ever the wrong size in your terminal emulator run 
-- this to set the LINES and COLUMNS shell variables properly.
-- This only works when called from lua_console_hook, below.
function resize ()
    return "run", "eval resize"
end

-- Table of expressions which are recognised by our lua_console_hook.
console_hook_functions = {
    reload	= "reload ()",
    lpr		= "lpr ()",
    enscript	= "enscript ()",
    monitor	= monitor,
    mutt	= mutt,
    netscape	= "netscape ()",
    nuts	= "netscape ()",
    resize	= resize
}

function lua_console_hook (expr)
    local x = console_hook_functions[expr] 
    if type (x) == "function" then
	return x ()
    else
	return "eval", x or expr
    end
end


----------------------------------------------------------------------
--  quit_hook
----------------------------------------------------------------------

-- We need to delete the temporary files that we create.
if not tmp_files then
    tmp_files = {}
end

function quit_hook ()
    if bookmark_addon then
	bm_save_bookmarks ()
    end
    
    if tmp_files and remove then
        tmp_files.n = nil
        for i,v in tmp_files do remove (v) end
    end
end


----------------------------------------------------------------------
--  Examples of keybinding
----------------------------------------------------------------------

-- Bind Ctrl-H to a "Home" page.

--    bind_key ("main", "Ctrl-H",
--	      function () return "goto_url", "http://www.google.com/" end)

-- Bind Alt-p to print.

--    bind_key ("main", "Alt-p", lpr)

-- Bind Alt-m to toggle ALT="" mangling.

--    bind_key ("main", "Alt-m",
--	      function () mangle_blank_alt = not mangle_blank_alt end)


----------------------------------------------------------------------
--  Bookmark addon
----------------------------------------------------------------------

if bookmark_addon then

    dofile ("/usr/share/elinks/elinks-bm.lua")

    -- Add/change any bookmark options here.

    -- Be careful not to load bookmarks if this script is being
    -- reloaded while in Links, or we will lose unsaved changes.
    if not bm_bookmarks or getn (bm_bookmarks) == 0 then
	bm_load_bookmarks ()
    end

    -- My bookmark key bindings.
    bind_key ('main', 'a', bm_add_bookmark)
    bind_key ('main', 's', bm_view_bookmarks)
    bind_key ('main', 'Alt-e', bm_edit_bookmark)
    bind_key ('main', 'Alt-d', bm_delete_bookmark)
    bind_key ('main', 'Alt-k', bm_move_bookmark_up)
    bind_key ('main', 'Alt-j', bm_move_bookmark_down)

end


-- vim: shiftwidth=4 softtabstop=4
