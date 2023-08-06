# Majel

A [Mycroft](https://mycroft.ai/) extension that lets you do visual things with
it as well.

![Architecture](https://gitlab.com/danielquinn/majel/-/raw/ff49bdfb8d6da025788dfe39a0fc13182ec4d0b1/architecture.png)


## What can it do?

Majel listens to the [Mycroft message bus framework](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/message-bus)
and performs various desktop jobs based on what it comes down that pipe.  The
result is that you get Mycroft's standard skills along with:


### Youtube player

Say `Hey Mycroft, youtube <query>` and it'll search Youtube for your `query`,
pick the first hit, and play it full screen in a loop.


### Kodi

If you've got a local Kodi installation *and* the video files you've got in
there are also mounted locally, you can say `Hey Mycroft, play <query>` and
it'll look for `query` in your Kodi library.  If it finds it, it'll play it
with `mpv` locally.  It's also smart enough to know which episodes you've seen,
so if you say `Hey Mycroft play Star Trek Deep Space Nine` and you've already
seen all of season 4, it'll start with s05e01.  It'll also pick up right where
you left off in that episode.


### Netflix & Amazon Prime

The `play` keyword will also fall back to Netflix or Amazon Prime if you don't
have Kodi installed, or simply don't have the video you were asking for.  In
this case, it'll hit up the [Utelly API](https://rapidapi.com/utelly/api/utelly)
to see which streaming service has the movie/show you asked for, and then point
your browser to that show and play the next episode.

Note that this functionality requires two things: a Utelly API key (it's free
for limited use, and we've got built-in caching so you'll never break the
1000/mo limit) and a subscription to Netflix and/or Amazon Prime.


### Browser Bookmarks

If you store your bookmarks in Firefox, you can say
`Hey Mycroft, search my bookmarks for <query>`.  This will rank your bookmarks
by relevance to your query and display a list of everything it found within a
threshold.  The list appears as a touchscreen-friendly UI so you can say *"Hey
Mycroft, search my bookmarks for chicken"* and select from your 12 favourite
chicken recipes.


## Configurability

Configuration of the skills is done separately for each skill via Mycroft's
standard settings UI on their site.  That's where, for example, you input your
YouTube API key and Utelly API key.

Majel is configured by way of your environment, so you can set that any way you
like.


## What's Next?

It'd be nice to have support for doing video calls: `Hey Mycroft, call the
parents`, but that may not be easy to do since most video calling platforms
seem to either be centred around scheduled group chat, or just plain
Linux/browser hostile.


## Colophon

For [Majel Barrett-Roddenberry](https://en.wikipedia.org/wiki/Majel_Barrett),
who was amazing.
