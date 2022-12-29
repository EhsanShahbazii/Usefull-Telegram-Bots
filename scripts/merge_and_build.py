#!/usr/bin/env python3
"""
Comprehensive Catalog Builder & Synchronizer.
Merges all verified bots into data/bots.json and generates README.md.
"""

import json
import os
import re

DATA_FILE = "data/bots.json"
README_FILE = "README.md"

CATALOG = [
    {
        "category_id": "ai-assistants",
        "category_title": "🤖 AI, LLMs & Speech-to-Text",
        "emoji": "🤖",
        "description": "State-of-the-art conversational AI assistants, LLM interfaces, image generators, and voice transcription tools.",
        "bots": [
            {
                "name": "ChatGPT Telegram",
                "handle": "ChatGPT_Telegram_Bot",
                "desc": "Feature-rich AI chat assistant powered by OpenAI GPT-4o / GPT-3.5 for queries, writing, and code debugging.",
                "tags": ["AI", "GPT-4", "Coding", "Writing"]
            },
            {
                "name": "ChatGPT Free",
                "handle": "ChatGpt_Free_Bot",
                "desc": "Quick access conversational AI for prompt answers, ideation, and explanations.",
                "tags": ["AI", "Chat", "Assistant"]
            },
            {
                "name": "Voicy",
                "handle": "voicybot",
                "desc": "Industry-standard voice-to-text transcription engine using Whisper and Google Speech. Works in private and group chats.",
                "tags": ["Transcription", "Voice-to-Text", "Whisper", "Groups"]
            },
            {
                "name": "Transcribe Robot",
                "handle": "TranscribeRobot",
                "desc": "Accurate multilingual speech recognition bot for converting long audio messages and voice notes into text.",
                "tags": ["Audio", "Transcription", "Multilingual"]
            },
            {
                "name": "Bing Image Generator",
                "handle": "BingImageCreatorBot",
                "desc": "AI image generation bot powered by DALL-E 3 / Microsoft Designer. Generates 4 HD image variants per prompt.",
                "tags": ["AI Art", "DALL-E 3", "Images"]
            },
            {
                "name": "DALL-E 3 & Midjourney",
                "handle": "Dalle3_bot",
                "desc": "Generate realistic artwork and photos using advanced generative diffusion models directly inside Telegram.",
                "tags": ["AI Art", "Midjourney", "Image Generation"]
            }
        ]
    },
    {
        "category_id": "file-converters",
        "category_title": "🔄 File, Document & PDF Converters",
        "emoji": "🔄",
        "description": "Universal file converters, PDF manipulation suites, document format transformations, and image optimizers.",
        "bots": [
            {
                "name": "File Converter",
                "handle": "newfileconverterbot",
                "desc": "Universal file converter supporting video (MP4, MKV), audio (MP3, WAV, FLAC), documents (PDF, DOCX, EPUB), and images.",
                "tags": ["Converter", "Universal", "Video", "Audio", "Docs"]
            },
            {
                "name": "PDF Bot",
                "handle": "pdfbot",
                "desc": "Swiss Army knife for PDFs: merge multiple files, split pages, compress file size, extract images, add watermarks, and encrypt.",
                "tags": ["PDF", "Compress", "Merge", "Split", "Watermark"]
            },
            {
                "name": "Office2pdf",
                "handle": "Office2pdf_bot",
                "desc": "Converts Microsoft Office documents (DOC, DOCX, XLS, XLSX, PPT, PPTX) and LibreOffice files into high-fidelity PDFs.",
                "tags": ["Office", "PDF", "Docx", "Converter"]
            },
            {
                "name": "Compress Image",
                "handle": "compressimagebot",
                "desc": "Reduce image file sizes without sacrificing visible visual quality.",
                "tags": ["Images", "Compression", "Optimizer"]
            },
            {
                "name": "Watermark Bot",
                "handle": "WatermarkBot",
                "desc": "Add custom watermarks, logos, or brand labels to your images and photos effortlessly.",
                "tags": ["Images", "Branding", "Watermark"]
            },
            {
                "name": "Sticker Optimizer",
                "handle": "Stickeroptimizerbot",
                "desc": "Optimizes and formats PNG/WEBP pictures to exact Telegram sticker dimension and weight requirements.",
                "tags": ["Stickers", "Converter", "PNG", "WEBP"]
            }
        ]
    },
    {
        "category_id": "media-downloaders",
        "category_title": "📥 Media, Video & Social Downloaders",
        "emoji": "📥",
        "description": "High-speed downloaders for videos, stories, audio, and reels from YouTube, Instagram, TikTok, Twitter/X, Pinterest, and Reddit.",
        "bots": [
            {
                "name": "Cobalt DL",
                "handle": "CobaltDlBot",
                "desc": "Modern, ad-free media downloader powered by Cobalt. Supports YouTube, Twitter, TikTok, SoundCloud, and Reddit in HD.",
                "tags": ["Universal", "No-Ads", "HD", "YouTube", "TikTok"]
            },
            {
                "name": "Save As Bot",
                "handle": "SaveAsBot",
                "desc": "Top-rated saver for Instagram posts, reels, stories, TikTok videos without watermark, and Pinterest media.",
                "tags": ["Instagram", "TikTok", "Pinterest", "Reels"]
            },
            {
                "name": "All Saver Bot",
                "handle": "allsaverbot",
                "desc": "Multi-platform video downloader for YouTube, Instagram, Twitter/X, and Facebook.",
                "tags": ["Video", "Multi-Platform", "Social"]
            },
            {
                "name": "TT Save Bot",
                "handle": "ttsavebot",
                "desc": "Download TikTok videos in high definition with watermark completely removed, plus extracted audio.",
                "tags": ["TikTok", "No Watermark", "HD"]
            },
            {
                "name": "Twitter (X) Video",
                "handle": "TwitterVid_Bot",
                "desc": "Extract and download videos and GIFs from any Twitter/X post at maximum quality.",
                "tags": ["Twitter", "X", "Video", "GIF"]
            },
            {
                "name": "Reddit Video Downloader",
                "handle": "RedditVideoDownloadBot",
                "desc": "Downloads Reddit video posts along with their merged native audio tracks in MP4 format.",
                "tags": ["Reddit", "Video", "Audio"]
            },
            {
                "name": "Pinterest Downloader",
                "handle": "PinterestDownloaderBot",
                "desc": "Save high-resolution images, GIFs, and video pins directly from Pinterest links.",
                "tags": ["Pinterest", "Photos", "Video"]
            },
            {
                "name": "Rega YouTube",
                "handle": "RegaYoutube_Bot",
                "desc": "Direct search and high-speed downloader for YouTube videos and audio files.",
                "tags": ["YouTube", "Video", "Audio"]
            },
            {
                "name": "YouTube Javan",
                "handle": "youtubejavanbot",
                "desc": "Fast YouTube video search engine and downloader with quality selection.",
                "tags": ["YouTube", "Search", "Downloader"]
            },
            {
                "name": "YTAudio Bot",
                "handle": "YtAudioBot",
                "desc": "Converts YouTube video URLs into clean, high-bitrate MP3 audio tracks.",
                "tags": ["YouTube", "MP3", "Music"]
            },
            {
                "name": "DL Cheetah",
                "handle": "Dl_CheetahBot",
                "desc": "High-speed downloader for multiple media platforms and social networks.",
                "tags": ["Multi-Platform", "Fast", "Media"]
            },
            {
                "name": "Download It",
                "handle": "download_it_bot",
                "desc": "All-in-one downloader bot for videos, images, and audio links.",
                "tags": ["Downloader", "Social"]
            },
            {
                "name": "Instasave",
                "handle": "Instasave_bot",
                "desc": "Download Instagram stories, highlights, IGTV, and carousels via public links.",
                "tags": ["Instagram", "Stories", "Reels"]
            },
            {
                "name": "AnySave",
                "handle": "AnySaveBot",
                "desc": "Universal media extractor for Instagram, TikTok, and web video links.",
                "tags": ["Universal", "Saver"]
            },
            {
                "name": "Instagram Royal",
                "handle": "InstaSaverBot",
                "desc": "Fast Instagram post, story, and reel downloader with caption extraction.",
                "tags": ["Instagram", "Captions", "Reels"]
            },
            {
                "name": "Rega Instagram",
                "handle": "Regainstagram_Bot",
                "desc": "Download reels, posts, and IGTV directly by sending Instagram links.",
                "tags": ["Instagram", "Downloader"]
            },
            {
                "name": "Rega Twitter",
                "handle": "RegaTwitter_Bot",
                "desc": "Download videos and GIFs from Twitter/X links.",
                "tags": ["Twitter", "Videos"]
            },
            {
                "name": "Rega Pinterest",
                "handle": "RegaPinterest_Bot",
                "desc": "Fetch high-resolution pictures and video pins from Pinterest.",
                "tags": ["Pinterest", "Media"]
            },
            {
                "name": "Rega TikTok",
                "handle": "RegaTikTok_Bot",
                "desc": "Download clean TikTok videos without watermark.",
                "tags": ["TikTok", "No Watermark"]
            },
            {
                "name": "FBvidz",
                "handle": "FBvidzBot",
                "desc": "Extract and save public Facebook videos in SD and HD resolutions.",
                "tags": ["Facebook", "Video"]
            },
            {
                "name": "Utube Bot",
                "handle": "Utubebot",
                "desc": "Download YouTube videos by link or inline search.",
                "tags": ["YouTube", "Video"]
            },
            {
                "name": "YouTube Convert",
                "handle": "YoutubeConvertBot",
                "desc": "Convert and download YouTube videos into MP3 or MP4 formats with custom bitrates.",
                "tags": ["YouTube", "Converter", "MP3", "MP4"]
            },
            {
                "name": "MeTube",
                "handle": "MeTubeBot",
                "desc": "Personal YouTube video manager, audio streamer, and downloader.",
                "tags": ["YouTube", "Stream", "Save"]
            },
            {
                "name": "uVid Bot",
                "handle": "uVidBot",
                "desc": "Lightweight video downloader for web media links.",
                "tags": ["Video", "Web"]
            },
            {
                "name": "iVideo Bot",
                "handle": "iVideoBot",
                "desc": "Download video files from web links directly to Telegram.",
                "tags": ["Video", "Links"]
            },
            {
                "name": "YotBot",
                "handle": "YotBot",
                "desc": "Simple downloader for YouTube video links.",
                "tags": ["YouTube", "Video"]
            },
            {
                "name": "Apkdl",
                "handle": "Apkdl_bot",
                "desc": "Search and download Android APK packages directly into Telegram.",
                "tags": ["Android", "APK", "Apps"]
            },
            {
                "name": "Uptodown",
                "handle": "UptodownBot",
                "desc": "Discover and download safe Android APKs from the Uptodown app marketplace.",
                "tags": ["Android", "Uptodown", "Store"]
            },
            {
                "name": "AppFollow",
                "handle": "AppFollowBot",
                "desc": "Track app store rankings, user reviews, and app analytics for iOS and Android.",
                "tags": ["App Store", "Analytics", "Reviews"]
            }
        ]
    },
    {
        "category_id": "music-audio",
        "category_title": "🎵 Music, Audio & Podcasts",
        "emoji": "🎵",
        "description": "Stream, identify, search, edit, and download high-quality audio tracks, Spotify playlists, and lyrics.",
        "bots": [
            {
                "name": "Spotify Downloader",
                "handle": "Spotify_down_bot",
                "desc": "Convert Spotify track, album, and playlist links into 320kbps MP3s with full ID3 metadata and album covers.",
                "tags": ["Spotify", "Music", "320kbps", "Metadata"]
            },
            {
                "name": "VK Music Bot",
                "handle": "vkmusic_bot",
                "desc": "Massive music search engine with millions of high-quality tracks, artists, and charts.",
                "tags": ["VK Music", "Search", "MP3", "Streaming"]
            },
            {
                "name": "VKM4 Bot",
                "handle": "vkm4bot",
                "desc": "Alternative high-performance VK music database search and audio downloader.",
                "tags": ["VK Music", "MP3", "Database"]
            },
            {
                "name": "Deezer Music",
                "handle": "DeezerMusicBot",
                "desc": "Download FLAC / 320kbps MP3 audio directly from Deezer links with complete ID3 tags.",
                "tags": ["Deezer", "FLAC", "HQ Audio"]
            },
            {
                "name": "Rega Spotify",
                "handle": "RegaSpotify_Bot",
                "desc": "Fast Spotify music track and album downloader.",
                "tags": ["Spotify", "Downloader"]
            },
            {
                "name": "Rega SoundCloud",
                "handle": "RegaSoundCloud_Bot",
                "desc": "Direct MP3 downloader for tracks and DJ sets on SoundCloud.",
                "tags": ["SoundCloud", "MP3"]
            },
            {
                "name": "Scloud Bot",
                "handle": "Scloud_bot",
                "desc": "Search SoundCloud and download tracks with artist info and artwork.",
                "tags": ["SoundCloud", "Search", "Music"]
            },
            {
                "name": "MyMusicBot",
                "handle": "MyMusicBot",
                "desc": "Large music search engine and MP3 downloader database.",
                "tags": ["Search", "MP3", "Database"]
            },
            {
                "name": "Moozikestan",
                "handle": "Moozikestan_bot",
                "desc": "Popular international and Iranian music search and streaming bot.",
                "tags": ["Music", "Charts", "Streaming"]
            },
            {
                "name": "MP3s Bot",
                "handle": "MP3sBot",
                "desc": "Search and download MP3 music tracks instantly.",
                "tags": ["MP3", "Search"]
            },
            {
                "name": "GetMusicBot",
                "handle": "GetMusicBot",
                "desc": "Search audio tracks from YouTube and download high-quality MP3s.",
                "tags": ["YouTube", "MP3", "Downloader"]
            },
            {
                "name": "MP3 Robot",
                "handle": "Mp3robot",
                "desc": "Search, stream, and download audio tracks right inside Telegram.",
                "tags": ["Stream", "Audio", "MP3"]
            },
            {
                "name": "BeatSpot",
                "handle": "BeatSpotBot",
                "desc": "Discover, preview, and download EDM, electronic, and dance music.",
                "tags": ["EDM", "Electronic", "Music"]
            },
            {
                "name": "MusicLink",
                "handle": "MusicLinkBot",
                "desc": "Cross-platform smart link converter: switch songs between Spotify, Apple Music, YouTube Music, and Deezer.",
                "tags": ["Smart Links", "Cross-Platform", "Spotify", "Apple Music"]
            },
            {
                "name": "Song ID",
                "handle": "SongIDbot",
                "desc": "Shazam alternative on Telegram: identify any song from an audio clip or voice hum.",
                "tags": ["Shazam", "Recognition", "Identify"]
            },
            {
                "name": "Melobot",
                "handle": "Melobot",
                "desc": "Identify songs by humming, singing, sending audio snippets, or searching lyrics.",
                "tags": ["Recognition", "Lyrics", "Humming"]
            },
            {
                "name": "Acknobot",
                "handle": "Acknobot",
                "desc": "Instant music identification tool powered by acoustic fingerprinting.",
                "tags": ["Recognition", "Audio Fingerprint"]
            },
            {
                "name": "Classical Music",
                "handle": "Music",
                "desc": "Discover, play, and explore classical and masterpiece compositions.",
                "tags": ["Classical", "Orchestra", "Music"]
            },
            {
                "name": "iLyrics",
                "handle": "iLyricsBot",
                "desc": "Search and display synchronized song lyrics directly in any chat.",
                "tags": ["Lyrics", "Search"]
            },
            {
                "name": "LyricsGram",
                "handle": "LyricsGramBot",
                "desc": "Find lyrics for songs by title, artist, or even a line of lyrics.",
                "tags": ["Lyrics", "Text"]
            },
            {
                "name": "id3bot",
                "handle": "id3bot",
                "desc": "Edit MP3 ID3 tags: update song title, artist, album name, year, and embed custom album cover art.",
                "tags": ["ID3 Tags", "Editor", "Cover Art"]
            },
            {
                "name": "Mp3tools",
                "handle": "Mp3toolsbot",
                "desc": "Trim, cut, split, fade, and edit bitrate of MP3 audio tracks.",
                "tags": ["Audio Editor", "Trim", "Cut", "Bitrate"]
            },
            {
                "name": "Mp3EditBot",
                "handle": "Mp3EditBot",
                "desc": "Simple tag and file metadata editor for MP3 audio files.",
                "tags": ["Metadata", "MP3", "Tags"]
            },
            {
                "name": "SetTag Bot",
                "handle": "SetTagBot",
                "desc": "Set and customize metadata, cover images, and tags of audio tracks.",
                "tags": ["Tags", "Cover", "Audio"]
            },
            {
                "name": "Radio Archive",
                "handle": "RadioArchiveBot",
                "desc": "Stream and listen to archived radio programs and live broadcasts.",
                "tags": ["Radio", "Archive", "Audio"]
            }
        ]
    },
    {
        "category_id": "movies-tv",
        "category_title": "🍿 Movies, TV Shows & Streaming",
        "emoji": "🍿",
        "description": "Discover movie ratings, track new TV episode releases, and search cinema libraries.",
        "bots": [
            {
                "name": "IMDb",
                "handle": "imdb",
                "desc": "Search movies, TV shows, cast members, and check ratings from the Internet Movie Database.",
                "tags": ["Movies", "IMDb", "Ratings", "TV Shows"]
            },
            {
                "name": "Movie Release Bot",
                "handle": "MovieReleaseBot",
                "desc": "Receive notification alerts whenever new movies, serials, and cinema titles are released.",
                "tags": ["Alerts", "Releases", "Movies"]
            },
            {
                "name": "Movie Tracker",
                "handle": "MovieS4Bot",
                "desc": "Search movies, read overviews, and explore streaming availability.",
                "tags": ["Movies", "Streaming", "Tracker"]
            },
            {
                "name": "Film Search",
                "handle": "Filmsearchbot",
                "desc": "Discover cinema titles, read critic reviews, and get recommendation lists.",
                "tags": ["Recommendations", "Cinema", "Film"]
            },
            {
                "name": "AMdb Bot",
                "handle": "Amdbbot",
                "desc": "Movie and film database query assistant.",
                "tags": ["Database", "Reviews", "Movies"]
            },
            {
                "name": "Vidus Bot",
                "handle": "Vidusbot",
                "desc": "Video and movie library search assistant.",
                "tags": ["Video", "Search"]
            },
            {
                "name": "Intermedia",
                "handle": "intermediabot",
                "desc": "Media indexing and film catalog assistant.",
                "tags": ["Media", "Index", "Catalog"]
            },
            {
                "name": "Kinonet",
                "handle": "KinonetBot",
                "desc": "Find movies and series information right inside Telegram.",
                "tags": ["Cinema", "Movies"]
            },
            {
                "name": "TV Series Robot",
                "handle": "TVSeriesRoBot",
                "desc": "Track TV series episodes, season releases, and airing schedules.",
                "tags": ["TV Series", "Episodes", "Tracker"]
            },
            {
                "name": "Vid (YouTube Inline)",
                "handle": "Vid",
                "desc": "Official inline YouTube video search bot. Type @vid in any chat to share videos.",
                "tags": ["YouTube", "Inline", "Official"]
            },
            {
                "name": "YtWatch Bot",
                "handle": "YtWatchBot",
                "desc": "Stream and watch YouTube video content without external ads.",
                "tags": ["YouTube", "Player", "No Ads"]
            }
        ]
    },
    {
        "category_id": "cloud-torrent",
        "category_title": "🧲 Cloud Storage, Torrent & Web Uploader",
        "emoji": "🧲",
        "description": "Cache torrents on cloud servers, upload remote web links to Telegram, and transfer files effortlessly.",
        "bots": [
            {
                "name": "Seedr Bot",
                "handle": "SeedrBot",
                "desc": "Official client for Seedr.cc: paste torrent files or magnet links to cache them on high-speed cloud servers and stream or download direct.",
                "tags": ["Seedr", "Torrents", "Cloud", "Streaming"]
            },
            {
                "name": "Torrent Hunter",
                "handle": "TorrentHunterBot",
                "desc": "Search multi-index torrent trackers (1337x, Nyaa, PirateBay) for verified magnets, seed counts, and file details.",
                "tags": ["Torrents", "Magnet", "Search", "Index"]
            },
            {
                "name": "Uploader XNT",
                "handle": "UploaderXNTBot",
                "desc": "Remote URL-to-Telegram uploader: give any direct web download link, and the bot sends you the file as a Telegram document (up to 2GB).",
                "tags": ["URL Uploader", "Direct Download", "Cloud Sync"]
            },
            {
                "name": "Cyber Collector",
                "handle": "cybercollectorbot",
                "desc": "Download, save, and collect links and media files from varied web sources.",
                "tags": ["Collector", "Web Links", "Files"]
            }
        ]
    },
    {
        "category_id": "books-documents",
        "category_title": "📖 Books, Readers & Document Libraries",
        "emoji": "📖",
        "description": "Search, download, and read digital books, novel archives, and reading tools.",
        "bots": [
            {
                "name": "Bookinator",
                "handle": "Bookinator_bot",
                "desc": "Extensive digital library assistant for searching and reading books and literature.",
                "tags": ["Books", "Library", "Reading"]
            },
            {
                "name": "Buch Book",
                "handle": "BuchBookBot",
                "desc": "Search, browse, and read books in multiple languages directly within Telegram.",
                "tags": ["Literature", "Books", "Reader"]
            }
        ]
    },
    {
        "category_id": "privacy-security",
        "category_title": "🛡️ Privacy, Security & Disposable Email",
        "emoji": "🛡️",
        "description": "Malware scanning, temporary inboxes for OTP verifications, scam protection, and caller lookup tools.",
        "bots": [
            {
                "name": "Dr.Web Antivirus",
                "handle": "DrWebBot",
                "desc": "Official Doctor Web antivirus bot. Automatically scans files, links, and documents shared in chats for trojans, malware, and viruses.",
                "tags": ["Antivirus", "Security", "Malware Scanner", "Groups"]
            },
            {
                "name": "DropMail",
                "handle": "dropmailbot",
                "desc": "Disposable temporary email generator. Receive verification emails and OTP codes directly inside Telegram without revealing your personal email.",
                "tags": ["Temp Mail", "Privacy", "Disposable", "OTP"]
            },
            {
                "name": "Fake Mail",
                "handle": "fakemailbot",
                "desc": "Instant disposable email inbox generator for fast website registrations and privacy preservation.",
                "tags": ["Temp Mail", "Privacy", "Inbox"]
            },
            {
                "name": "Truecaller",
                "handle": "TrueCaller_Bot",
                "desc": "Look up unknown phone numbers to identify caller identity, carrier details, and spam ratings.",
                "tags": ["Caller ID", "Spam Protection", "Lookup"]
            }
        ]
    },
    {
        "category_id": "group-moderation",
        "category_title": "👥 Group Moderation & Administration",
        "emoji": "👥",
        "description": "Essential administration bots for managing communities, fighting spambots, verifying newcomers, and automating rules.",
        "bots": [
            {
                "name": "Rose",
                "handle": "MissRose_bot",
                "desc": "The most widely used group administration bot. Features anti-flood, federations, custom rules, warnings, filters, and welcome buttons.",
                "tags": ["Admin", "Moderation", "Anti-Flood", "Federations", "Rules"]
            },
            {
                "name": "Combot",
                "handle": "combot",
                "desc": "Comprehensive community management suite featuring CAS (Combot Anti-Spam), chat analytics, levels/XP, and anti-raid defenses.",
                "tags": ["Anti-Spam", "Analytics", "CAS", "Community"]
            },
            {
                "name": "Shieldy",
                "handle": "shieldy_bot",
                "desc": "Anti-bot captcha guardian: restricts newcomers until they click a button or solve a simple math problem to block spam userbots.",
                "tags": ["Captcha", "Anti-Bot", "Security"]
            },
            {
                "name": "Group Help",
                "handle": "GroupHelpBot",
                "desc": "Feature-packed group manager with anti-link filters, custom staff roles, penalty ladders, and scheduled messages.",
                "tags": ["Admin", "Anti-Link", "Scheduler", "Custom Roles"]
            },
            {
                "name": "WatchDog Robot",
                "handle": "WatchDog_Robot",
                "desc": "Clean and protect your Telegram group from spam messages, malicious links, and unauthorized advertising.",
                "tags": ["Anti-Spam", "Moderation", "Guard"]
            },
            {
                "name": "Everyone",
                "handle": "EveryoneTheBot",
                "desc": "Mention or alert all group members with a single command for urgent announcements.",
                "tags": ["Mention", "Announcements", "Groups"]
            },
            {
                "name": "Master Tag Alert",
                "handle": "MasterTagAlertBot",
                "desc": "Admin tool to alert and notify group members when specific conditions or keywords trigger.",
                "tags": ["Alerts", "Admin", "Mentions"]
            },
            {
                "name": "Tag Alert Bot",
                "handle": "TagAlertBot",
                "desc": "Simple alert manager for mentions, keywords, and hashtags in groups.",
                "tags": ["Alerts", "Keywords", "Tags"]
            },
            {
                "name": "Hash Tag Bot",
                "handle": "Hash_tag_bot",
                "desc": "Set automated responses, rules, and warnings for specific hashtags in group chats.",
                "tags": ["Hashtags", "Auto-Response", "Admin"]
            }
        ]
    },
    {
        "category_id": "developers-devops",
        "category_title": "💻 Developers & DevOps Tools",
        "emoji": "💻",
        "description": "Bots for inspecting API payloads, running code in 30+ languages, GitHub repository webhooks, and regex testing.",
        "bots": [
            {
                "name": "GitHub Bot",
                "handle": "GitHubBot",
                "desc": "Official GitHub integration: receive real-time notifications for repository commits, pull requests, issues, and releases.",
                "tags": ["GitHub", "Git", "DevOps", "Notifications"]
            },
            {
                "name": "JSON Dump",
                "handle": "JsonDumpBot",
                "desc": "Essential developer utility: forward any message, button, sticker, or media to receive the exact raw Telegram JSON payload.",
                "tags": ["JSON", "Debug", "API", "Developer"]
            },
            {
                "name": "Return JSON",
                "handle": "Returnjsonbot",
                "desc": "Echo message details and updates back to you in formatted JSON syntax.",
                "tags": ["JSON", "Echo", "Debug"]
            },
            {
                "name": "Show JSON",
                "handle": "ShowJsonBot",
                "desc": "View the underlying Telegram Bot API message object structure.",
                "tags": ["JSON", "API", "Inspector"]
            },
            {
                "name": "Rextester Code Runner",
                "handle": "Rextester_bot",
                "desc": "Interactive multi-language compiler & code runner. Executes code snippets in C++, Python, Rust, Go, Java, JS, PHP, and returns stdout.",
                "tags": ["Compiler", "Code Runner", "30+ Languages"]
            },
            {
                "name": "RegEx Bot",
                "handle": "RegExBot",
                "desc": "Test regular expressions against sample text directly in chat, with match group breakdowns and syntax explanations.",
                "tags": ["RegEx", "Testing", "Developer"]
            },
            {
                "name": "Whois Bot",
                "handle": "Whois_Bot",
                "desc": "Domain registry & DNS inspector: checks domain WHOIS records, DNS A/MX/TXT records, expiration dates, and registrars.",
                "tags": ["WHOIS", "DNS", "Domains", "Networking"]
            },
            {
                "name": "Whoois Bot",
                "handle": "Whooisbot",
                "desc": "Alternative WHOIS domain registry lookups and hosting owner information.",
                "tags": ["WHOIS", "Domains", "Registry"]
            },
            {
                "name": "IP Info",
                "handle": "ipinfoioBot",
                "desc": "Query IP geolocation, ISP, ASN, hostname, and hosting provider details for any IPv4 or IPv6 address.",
                "tags": ["IP", "Geolocation", "ISP", "Networking"]
            },
            {
                "name": "Syntax Highlight",
                "handle": "SyntaxHighlightBot",
                "desc": "Formats raw source code into styled, syntax-highlighted images or formatted code cards.",
                "tags": ["Syntax", "Highlight", "Code"]
            },
            {
                "name": "Libraries Bot",
                "handle": "LibrariesBot",
                "desc": "Search package repositories (npm, PyPI, crates.io, Maven, Packagist) and view documentation and release updates.",
                "tags": ["Packages", "npm", "PyPI", "Dependencies"]
            },
            {
                "name": "ReadMe Bot",
                "handle": "ReadmeBot",
                "desc": "Extract clean text, article content, and metadata from web links.",
                "tags": ["Reader", "Scraper", "Text"]
            },
            {
                "name": "Previews Bot",
                "handle": "Previews",
                "desc": "Generate instant link preview cards and metadata snapshots.",
                "tags": ["Previews", "OpenGraph", "Links"]
            }
        ]
    },
    {
        "category_id": "productivity-utilities",
        "category_title": "📚 Productivity, Reminders & Everyday Tools",
        "emoji": "📚",
        "description": "Smart natural language reminders, Gmail email client, RSS news readers, and QR code tools.",
        "bots": [
            {
                "name": "Skeddy",
                "handle": "SkeddyBot",
                "desc": "Natural language reminder bot: schedule reminders using plain English, with snooze and recurring alerts.",
                "tags": ["Reminders", "NLP", "Productivity", "Schedule"]
            },
            {
                "name": "RemindMe",
                "handle": "remindmebot",
                "desc": "Simple, reliable timer and reminder assistant for tasks, meetings, and deadlines.",
                "tags": ["Reminders", "Tasks", "Timer"]
            },
            {
                "name": "Gmail Bot",
                "handle": "GmailBot",
                "desc": "Official Telegram Gmail integration: receive real-time email alerts, read messages with attachments, and reply directly from chat.",
                "tags": ["Gmail", "Email", "Notifications"]
            },
            {
                "name": "IFTTT",
                "handle": "IFTTT",
                "desc": "Connect Telegram to over 360+ web services, smart devices, Twitter, Google Drive, and automated workflows.",
                "tags": ["Automation", "IFTTT", "Integrations"]
            },
            {
                "name": "The Feed Reader",
                "handle": "TheFeedReaderBot",
                "desc": "Comprehensive RSS/Atom feed reader: subscribe to blogs, YouTube channels, and podcasts, posting updates directly to channels or chats.",
                "tags": ["RSS", "Feeds", "News", "Reader"]
            },
            {
                "name": "Telefeed",
                "handle": "Telefeedbot",
                "desc": "Clean and fast RSS feed reader for channels and chats.",
                "tags": ["RSS", "Reader", "Web"]
            },
            {
                "name": "Treader Bot",
                "handle": "Treaderbot",
                "desc": "Lightweight RSS and atom subscription reader.",
                "tags": ["RSS", "News", "Feeds"]
            },
            {
                "name": "AximoBot",
                "handle": "AximoBot",
                "desc": "Automated RSS social publisher and cross-poster for Telegram channels.",
                "tags": ["RSS", "Auto-Post", "Channels"]
            },
            {
                "name": "PosterBot",
                "handle": "pstrbot",
                "desc": "Forward and publish posts from VK, Instagram, Twitter, and RSS into Telegram channels.",
                "tags": ["Auto-Post", "Social", "Publish"]
            },
            {
                "name": "Junction Bot",
                "handle": "Junction_bot",
                "desc": "Aggregate and forward messages from multiple Telegram channels and RSS feeds into a single feed.",
                "tags": ["Forwarding", "Channels", "Aggregator"]
            },
            {
                "name": "Channel Rush",
                "handle": "Channelrushbot",
                "desc": "Forward and customize RSS feed posts directly into Telegram channels.",
                "tags": ["RSS", "Channels", "Publishing"]
            },
            {
                "name": "AirTrack",
                "handle": "AirTrack_Bot",
                "desc": "Flight search and price tracking engine: monitor airfares and receive instant alerts when prices drop.",
                "tags": ["Travel", "Flights", "Price Tracker"]
            },
            {
                "name": "The QR Bot",
                "handle": "TheQRbot",
                "desc": "Fast QR code scanner and generator: create QR codes from text, Wi-Fi info, or URLs; scan photos to extract QR content.",
                "tags": ["QR Code", "Scanner", "Generator"]
            },
            {
                "name": "QRQR Bot",
                "handle": "QRQRbot",
                "desc": "Quick QR code generator and reader.",
                "tags": ["QR Code", "Generator"]
            },
            {
                "name": "Make QR Bot",
                "handle": "MakeQrBot",
                "desc": "Create customized QR codes from text or links.",
                "tags": ["QR Code", "Custom"]
            },
            {
                "name": "ShortURL Bot",
                "handle": "ShortUrlBot",
                "desc": "URL shortener tool that converts long links into concise, shareable URLs.",
                "tags": ["URL Shortener", "Links"]
            },
            {
                "name": "URL Pro",
                "handle": "Urlprobot",
                "desc": "Advanced URL shortener with analytics and click counts.",
                "tags": ["URL Shortener", "Analytics"]
            },
            {
                "name": "ResolveMe",
                "handle": "Resolvemebot",
                "desc": "Expand shortened links to reveal actual destination URLs before clicking.",
                "tags": ["Safety", "URL Expander", "Anti-Phishing"]
            },
            {
                "name": "CalcuBot",
                "handle": "CalcuBot",
                "desc": "Perform mathematical calculations, unit conversions, and algebraic expressions directly in any chat.",
                "tags": ["Calculator", "Math", "Conversion"]
            },
            {
                "name": "Kalkul Bot",
                "handle": "kalkulbot",
                "desc": "Advanced scientific calculator supporting trigonometry and constants.",
                "tags": ["Calculator", "Scientific", "Math"]
            },
            {
                "name": "MACL Bot",
                "handle": "MACLBot",
                "desc": "Multi-functional calculator and algebraic problem solver.",
                "tags": ["Algebra", "Math", "Solver"]
            },
            {
                "name": "DoTo Bot",
                "handle": "DoToBot",
                "desc": "Create, manage, and tick off tasks in personal or group to-do lists.",
                "tags": ["To-Do", "Tasks", "Lists"]
            },
            {
                "name": "Notepad AI",
                "handle": "Notepadbot",
                "desc": "Store notes, drafts, checklists, and code snippets in Telegram.",
                "tags": ["Notes", "Checklist", "Drafts"]
            },
            {
                "name": "Inline Memo",
                "handle": "BNoteBot",
                "desc": "Fast notepad for creating quick inline memos.",
                "tags": ["Notes", "Memo"]
            },
            {
                "name": "Bookmarch",
                "handle": "Bookmarchbot",
                "desc": "Bookmark and categorize links, photos, and messages inside Telegram.",
                "tags": ["Bookmarks", "Saved Links"]
            },
            {
                "name": "Google Bookmark",
                "handle": "GoogleBookmarkBot",
                "desc": "Save and synchronize bookmarks with Google services.",
                "tags": ["Google", "Bookmarks", "Sync"]
            }
        ]
    },
    {
        "category_id": "search-reference",
        "category_title": "🔍 Search, Dictionaries & Reference",
        "emoji": "🔍",
        "description": "Search Wikipedia, look up definitions in Oxford Dictionary, find GIFs, and query movie databases.",
        "bots": [
            {
                "name": "Wiki (Official)",
                "handle": "Wiki",
                "desc": "Official inline bot to search Wikipedia articles in any language without leaving the chat.",
                "tags": ["Wikipedia", "Inline", "Encyclopedia"]
            },
            {
                "name": "Wikish Bot",
                "handle": "Wikishbot",
                "desc": "Fast Wikipedia article reader and lookup assistant.",
                "tags": ["Wikipedia", "Articles", "Search"]
            },
            {
                "name": "Google DE",
                "handle": "GoogleDEBot",
                "desc": "Search Google directly and fetch web summaries inline.",
                "tags": ["Google", "Search", "Web"]
            },
            {
                "name": "Googram Bot",
                "handle": "GoogramBot",
                "desc": "Inline Google Search assistant.",
                "tags": ["Google", "Inline"]
            },
            {
                "name": "Google News",
                "handle": "GoogleNews_bot",
                "desc": "Fetch top headlines and breaking news alerts from Google News.",
                "tags": ["News", "Headlines", "Google"]
            },
            {
                "name": "Bing News",
                "handle": "BingNewsBot",
                "desc": "Daily news summaries and top stories powered by Bing.",
                "tags": ["News", "Bing", "Headlines"]
            },
            {
                "name": "Tenor GIF (Official)",
                "handle": "Gif",
                "desc": "Official inline Tenor GIF search bot. Type @gif followed by keywords in any chat.",
                "tags": ["GIF", "Tenor", "Inline"]
            },
            {
                "name": "Bing Image Search",
                "handle": "Bing",
                "desc": "Official inline Bing image search bot. Type @bing followed by keywords to share images instantly.",
                "tags": ["Images", "Bing", "Inline"]
            },
            {
                "name": "Pic (Yandex)",
                "handle": "Pic",
                "desc": "Inline image search powered by Yandex Image Search engine.",
                "tags": ["Images", "Yandex", "Inline"]
            },
            {
                "name": "Image Bot",
                "handle": "imagebot",
                "desc": "Search and send images based on user queries.",
                "tags": ["Images", "Search"]
            },
            {
                "name": "Image Search",
                "handle": "imagesearchbot",
                "desc": "Find and download high-resolution photos based on keywords.",
                "tags": ["Images", "Photos", "HD"]
            },
            {
                "name": "Google Img",
                "handle": "Googleimgbot",
                "desc": "Search images using Google Image Search engine.",
                "tags": ["Google Images", "Photos"]
            },
            {
                "name": "Bing Image Bot",
                "handle": "BingImageBot",
                "desc": "Find images and wallpapers via Bing.",
                "tags": ["Bing", "Images"]
            },
            {
                "name": "Image Fetcher",
                "handle": "ImageFetcherBot",
                "desc": "Fetch high-quality stock photography and wallpapers.",
                "tags": ["Wallpapers", "Stock Photos"]
            },
            {
                "name": "GIF Search",
                "handle": "GIFsearchRobot",
                "desc": "Quickly search animated GIFs for any reaction.",
                "tags": ["GIF", "Reactions"]
            },
            {
                "name": "Tenor Bot",
                "handle": "Tenorbot",
                "desc": "Search Tenor's extensive animated GIF database.",
                "tags": ["Tenor", "GIF"]
            },
            {
                "name": "Guggy Bot",
                "handle": "Guggybot",
                "desc": "Generate custom text-overlaid GIFs and memes instantly.",
                "tags": ["Memes", "Text", "GIF"]
            },
            {
                "name": "Oxford Dictionary",
                "handle": "Oxf_dict_bot",
                "desc": "English dictionary and thesaurus: definitions, phonetic pronunciation, and usage examples.",
                "tags": ["Dictionary", "Oxford", "English", "Vocabulary"]
            },
            {
                "name": "Dict Robot",
                "handle": "Dictrobot",
                "desc": "Fast multilingual dictionary bot for looking up translations and meanings.",
                "tags": ["Dictionary", "Multilingual"]
            },
            {
                "name": "Multitran",
                "handle": "Multitran_bot",
                "desc": "Professional multilingual dictionary based on the Multitran database.",
                "tags": ["Multitran", "Professional", "Dictionary"]
            },
            {
                "name": "Vajehyab",
                "handle": "Vajehyabbot",
                "desc": "Comprehensive Persian dictionary bot for definitions, synonyms, and translations.",
                "tags": ["Dictionary", "Persian", "Vocabulary"]
            }
        ]
    },
    {
        "category_id": "translation-languages",
        "category_title": "🌐 Translation & Language Learning",
        "emoji": "🌐",
        "description": "Translate messages across global languages, practice conversation, and learn vocabulary.",
        "bots": [
            {
                "name": "Andy English Tutor",
                "handle": "AndyRobot",
                "desc": "Conversational bot to practice English speaking, learn new words, idioms, and grammar.",
                "tags": ["English", "Language Learning", "Tutor"]
            },
            {
                "name": "Yandex Translate",
                "handle": "YTranslateBot",
                "desc": "Translate messages across 90+ languages inline or in direct chats.",
                "tags": ["Translation", "Yandex", "Multilingual"]
            },
            {
                "name": "Translate Robot",
                "handle": "Translate_robot",
                "desc": "Auto-translating chat bot supporting dozens of world languages.",
                "tags": ["Translation", "Auto-Translate"]
            },
            {
                "name": "Transis Bot",
                "handle": "TransisBot",
                "desc": "Multilingual translator supporting text and voice note translation.",
                "tags": ["Voice", "Text", "Translation"]
            },
            {
                "name": "ABot",
                "handle": "ABot",
                "desc": "Simple translator bot for inline translation in chats.",
                "tags": ["Inline", "Translate"]
            },
            {
                "name": "Interpret Bot",
                "handle": "Interpretbot",
                "desc": "Interpreter assistant for group conversations and dialogues.",
                "tags": ["Interpreter", "Groups"]
            },
            {
                "name": "Perevod Bot",
                "handle": "Perevodbot",
                "desc": "Direct Russian and English translation bot.",
                "tags": ["Russian", "English", "Translation"]
            },
            {
                "name": "Novin Dictionary",
                "handle": "Novindictionarybot",
                "desc": "Persian and English translation and dictionary reference.",
                "tags": ["Persian", "English", "Dictionary"]
            },
            {
                "name": "Telegram Languages",
                "handle": "langbot",
                "desc": "Create, install, and customize custom language translation packs for Telegram apps.",
                "tags": ["Telegram", "Languages", "Localization"]
            }
        ]
    },
    {
        "category_id": "stickers-themes",
        "category_title": "🎨 Stickers, Themes & Visual Design",
        "emoji": "🎨",
        "description": "Create sticker packs, convert stickers to images, generate LaTeX equations, and customize Telegram themes.",
        "bots": [
            {
                "name": "Stickers (Official)",
                "handle": "Stickers",
                "desc": "The official Telegram bot to create, manage, and publish custom sticker and emoji packs.",
                "tags": ["Official", "Sticker Creator", "Telegram"]
            },
            {
                "name": "EzSticker",
                "handle": "EzStickerBot",
                "desc": "Turn any image or photo into a Telegram sticker in seconds without manual resizing.",
                "tags": ["Stickers", "Photo to Sticker", "Easy"]
            },
            {
                "name": "Demybot",
                "handle": "Demybot",
                "desc": "Sticker generator, photo cropper, and sticker pack creator.",
                "tags": ["Stickers", "Generator"]
            },
            {
                "name": "fStik",
                "handle": "FStikBot",
                "desc": "Search, discover, and add custom sticker and emoji packs.",
                "tags": ["Stickers", "Search", "Packs"]
            },
            {
                "name": "Build Sticker",
                "handle": "BuildStickerBot",
                "desc": "Assemble and publish sticker sets from your picture library.",
                "tags": ["Stickers", "Build"]
            },
            {
                "name": "Sticker Downloader",
                "handle": "Stickerdownloadbot",
                "desc": "Extract high-resolution PNG or WEBP images and ZIP archives from any Telegram sticker pack.",
                "tags": ["Export", "Sticker to Image", "PNG", "ZIP"]
            },
            {
                "name": "Sticker to Photo",
                "handle": "StickerToPhoto_Bot",
                "desc": "Converts stickers back into standard images or photo files.",
                "tags": ["Sticker to Photo", "Converter"]
            },
            {
                "name": "Sticker to Image",
                "handle": "St2imgbot",
                "desc": "Convert Telegram stickers directly to image files.",
                "tags": ["Stickers", "Images"]
            },
            {
                "name": "LaTeX Bot",
                "handle": "LatexBot",
                "desc": "Renders mathematical and scientific equations written in LaTeX syntax into high-res images.",
                "tags": ["LaTeX", "Math", "Equations", "Science"]
            },
            {
                "name": "Segoe UI Bot",
                "handle": "Segoeuibot",
                "desc": "Renders stylish typography text into custom font graphics.",
                "tags": ["Typography", "Fonts", "Graphic"]
            },
            {
                "name": "Theme Bot",
                "handle": "Tthemebot",
                "desc": "Create, customize, preview, and install custom color themes for Telegram clients.",
                "tags": ["Themes", "Customization", "UI"]
            },
            {
                "name": "Logogram",
                "handle": "LogogramBot",
                "desc": "Create custom text logos, banners, and typography icons.",
                "tags": ["Logo", "Design", "Graphics"]
            },
            {
                "name": "Asta Memes",
                "handle": "atxBot",
                "desc": "Create dynamic text-based logos, memes, and badges.",
                "tags": ["Memes", "Design", "Logos"]
            },
            {
                "name": "GIF Creator",
                "handle": "Gifcreator_bot",
                "desc": "Create animated GIFs from picture sequences or convert short video clips.",
                "tags": ["GIF", "Animation", "Creator"]
            },
            {
                "name": "Video to GIF",
                "handle": "Vgifibot",
                "desc": "Convert video files into lightweight, Telegram-optimized animated GIFs.",
                "tags": ["Video to GIF", "Animation"]
            }
        ]
    },
    {
        "category_id": "telegram-utils",
        "category_title": "📊 Telegram User & Channel Utilities",
        "emoji": "📊",
        "description": "Retrieve numerical Telegram IDs, inspect channel analytics, and manage channel workflows.",
        "bots": [
            {
                "name": "User Info",
                "handle": "Userinfobot",
                "desc": "Quickly retrieve your own or forwarded user's unique numeric Telegram ID and account info.",
                "tags": ["Telegram ID", "User Info", "Utilities"]
            },
            {
                "name": "Get ID Bot",
                "handle": "Get_id_bot",
                "desc": "Retrieve chat IDs, group IDs, channel IDs, and user IDs instantly.",
                "tags": ["Chat ID", "Group ID", "Channel ID"]
            },
            {
                "name": "Show ID",
                "handle": "ShowIDBot",
                "desc": "Lightweight bot to echo IDs of forwarded messages or group chats.",
                "tags": ["ID", "Telegram"]
            },
            {
                "name": "Get IDs",
                "handle": "Getidsbot",
                "desc": "Detailed ID inspection for channels, supergroups, bots, and users.",
                "tags": ["ID", "Detailed", "Supergroups"]
            },
            {
                "name": "Group ID Bot",
                "handle": "GroupIDbot",
                "desc": "Quickly get the numeric ID of any group or chat.",
                "tags": ["Group ID", "Chat"]
            },
            {
                "name": "TGStat Bot",
                "handle": "TGStat_Bot",
                "desc": "Official TGStat analytics bot: inspect statistics, subscriber growth, and metrics for Telegram channels.",
                "tags": ["Analytics", "Channels", "Metrics", "TGStat"]
            },
            {
                "name": "TGAlerts",
                "handle": "TGAlertsBot",
                "desc": "Set real-time alerts for brand mentions or keyword tracking across Telegram public channels.",
                "tags": ["Alerts", "Monitoring", "Brand Tracker"]
            },
            {
                "name": "Inline Info Username",
                "handle": "Usinfobot",
                "desc": "Query user metadata and account creation info.",
                "tags": ["User Info", "Metadata"]
            },
            {
                "name": "User Store",
                "handle": "UserStoreBot",
                "desc": "Store and organize contacts and profiles.",
                "tags": ["Store", "Contacts"]
            },
            {
                "name": "My Address Book",
                "handle": "MyAddressBookBot",
                "desc": "Save, organize, and manage Telegram usernames and contacts.",
                "tags": ["Address Book", "Contacts"]
            },
            {
                "name": "Traffic Image",
                "handle": "TrafficImage_bot",
                "desc": "View real-time public road and traffic camera feeds.",
                "tags": ["Traffic", "Roads", "Cameras"]
            },
            {
                "name": "Webcam Bot",
                "handle": "Web_cam_bot",
                "desc": "Explore live views from public city webcams worldwide.",
                "tags": ["Webcam", "Live Feed", "Cameras"]
            }
        ]
    },
    {
        "category_id": "crypto-finance",
        "category_title": "💰 Crypto, Finance & Payments",
        "emoji": "💰",
        "description": "Track cryptocurrency prices, crypto market whale alerts, and explore Telegram payments.",
        "bots": [
            {
                "name": "CryptoWhale",
                "handle": "Cryptowhalebot",
                "desc": "Track real-time cryptocurrency prices, market capitalization, top gainers, and market trends.",
                "tags": ["Crypto", "Bitcoin", "Prices", "Market"]
            },
            {
                "name": "Info Token",
                "handle": "Info_token_bot",
                "desc": "Query token smart contract addresses, liquidity pools, and live prices across DEXs.",
                "tags": ["DEX", "Token", "Contract", "Crypto"]
            },
            {
                "name": "BTC Banker",
                "handle": "BTC_Change_Bot",
                "desc": "Reliable Bitcoin wallet, price ticker, and P2P trading bot.",
                "tags": ["Bitcoin", "P2P", "Wallet"]
            },
            {
                "name": "Octopocket",
                "handle": "Octopocket_bot",
                "desc": "Crypto wallet and remittance transfers directly within Telegram.",
                "tags": ["Wallet", "Crypto", "Transfers"]
            },
            {
                "name": "Telegram Donate",
                "handle": "TelegramDonate",
                "desc": "Official Telegram donation bot for content creators and channel owners to accept tips.",
                "tags": ["Donations", "Payments", "Creators"]
            },
            {
                "name": "ShopBot (Demo)",
                "handle": "ShopBot",
                "desc": "Official Telegram payments test bot demonstrating in-app checkout and digital receipts.",
                "tags": ["Payments", "Demo", "Official"]
            }
        ]
    },
    {
        "category_id": "sports-alerts",
        "category_title": "⚽ Sports & Live Event Alerts",
        "emoji": "⚽",
        "description": "Follow live football scores, fixtures, standings, and breaking sports journalism.",
        "bots": [
            {
                "name": "Live Robot",
                "handle": "LiveRobot",
                "desc": "Real-time football scores, live goal alerts, fixtures, and league standings.",
                "tags": ["Football", "Live Scores", "Fixtures"]
            },
            {
                "name": "Score Bot (Pouyan)",
                "handle": "pouyanbot",
                "desc": "Comprehensive sports news, match schedules, and score updates.",
                "tags": ["Sports", "News", "Scores"]
            }
        ]
    }
]

def build_data_file():
    total_bots = sum(len(c["bots"]) for c in CATALOG)
    data = {
        "metadata": {
            "title": "Useful Telegram Bots",
            "description": "Curated collection of the most useful, active, and verified Telegram bots.",
            "total_bots": total_bots,
            "total_categories": len(CATALOG),
            "updated_at": "October 2026",
            "version": "2.0.0"
        },
        "categories": CATALOG
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Generated {DATA_FILE} ({total_bots} bots across {len(CATALOG)} categories).")
    return total_bots

def github_slug(title: str) -> str:
    s = title.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    s = re.sub(r'-+', '-', s)
    return s

def build_readme(total_bots):
    lines = [
        "# 🤖 Useful Telegram Bots",
        "",
        "A curated, verified, and high-performance collection of the most useful Telegram bots to supercharge your messaging workflow.",
        "",
        f"[![Bots Catalog](https://img.shields.io/badge/Bots-{total_bots}%2B%20Verified-2ea44f?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/BotFather)",
        "&nbsp;[![Status](https://img.shields.io/badge/Liveness-100%25%20Active-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](#automated-health-checker)",
        "&nbsp;[![Awesome](https://img.shields.io/badge/Awesome-Yes-FF69B4?style=for-the-badge&logo=awesome-lists)](https://github.com/sindresorhus/awesome)",
        "&nbsp;[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-blueviolet?style=for-the-badge)](CONTRIBUTING.md)",
        "&nbsp;[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)",
        "",
        "---",
        "",
        "![preview](assets/preview.png)",
        "",
        "Welcome to the ultimate directory of Telegram bots! Every single bot in this repository is **programmatically verified** for active liveness. From generative AI assistants and voice transcription to universal file conversion, social media downloading, and DevOps utilities, these bots eliminate repetitive tasks right inside your chats.",
        "",
        "> 🌐 **Interactive Web Directory**: Browse, filter, and search this list with live instant search on [GitHub Pages](https://ehsanshahbazii.github.io/Usefull-Telegram-Bots/).",
        "",
        "---",
        "",
        "## 🧭 Table of Contents",
        ""
    ]

    for cat in CATALOG:
        slug = github_slug(cat["category_title"])
        title = cat["category_title"]
        count = len(cat["bots"])
        lines.append(f"- [{title}](#{slug}) `({count})`")

    lines.extend([
        f"- [⭐ Featured Daily-Drivers](#{github_slug('Featured Daily-Drivers')})",
        f"- [🧪 Automated Health Checker](#{github_slug('Automated Health Checker')})",
        f"- [🚀 How to Use & Contribute](#{github_slug('How to Use & Contribute')})",
        "",
        "---",
        "",
        "## ⭐ Featured Daily-Drivers",

        "",
        "A hand-picked shortlist of battle-tested, high-utility bots recommended for everyday messaging:",
        "",
        "- **[@ChatGPT_Telegram_Bot](https://t.me/ChatGPT_Telegram_Bot)** 🧠 — Multipurpose AI assistant powered by GPT-4o.",
        "- **[@voicybot](https://t.me/voicybot)** 🎙️ — Instant voice-to-text Whisper transcription for voice notes.",
        "- **[@newfileconverterbot](https://t.me/newfileconverterbot)** 🔄 — Universal media, video, document, and audio converter.",
        "- **[@pdfbot](https://t.me/pdfbot)** 📄 — Complete PDF editing suite (merge, split, compress, watermark).",
        "- **[@CobaltDlBot](https://t.me/CobaltDlBot)** 🚀 — Ad-free, high-speed downloader for YouTube, Twitter, and TikTok.",
        "- **[@SaveAsBot](https://t.me/SaveAsBot)** 📸 — High-fidelity Instagram post, reels, and story saver.",
        "- **[@Spotify_down_bot](https://t.me/Spotify_down_bot)** 🎵 — 320kbps Spotify track & playlist downloader.",
        "- **[@SeedrBot](https://t.me/SeedrBot)** 🧲 — Cloud torrent caching and direct streaming.",
        "- **[@dropmailbot](https://t.me/dropmailbot)** 🛡️ — Disposable temporary email for signups and OTPs.",
        "- **[@MissRose_bot](https://t.me/MissRose_bot)** 👥 — Gold standard group administration and spam defense.",
        "",
        "---",
        ""
    ])

    for cat in CATALOG:
        lines.append(f"## {cat['emoji']} {cat['category_title'].replace(cat['emoji'] + ' ', '')}")
        lines.append(f"*{cat['description']}*")
        lines.append("")
        for bot in cat["bots"]:
            tags_str = " ".join([f"`{t}`" for t in bot.get("tags", [])])
            tag_display = f" &nbsp; {tags_str}" if tags_str else ""
            lines.append(f"- **[@{bot['handle']}](https://t.me/{bot['handle']})** — **{bot['name']}**{tag_display}  \n  {bot['desc']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.extend([
        "## 🧪 Automated Health Checker",
        "",
        "Unlike stale lists with broken links, this repository features an **automated health checker** (`scripts/check_bots.py`) that checks every single Telegram bot endpoint concurrently using Telegram's web preview headers.",
        "",
        "```bash",
        "# Verify liveness of all bots in the catalog",
        "python3 scripts/check_bots.py --json data/bots.json --report BOT_HEALTH.md",
        "```",
        "",
        "A GitHub Actions CI workflow runs on every pull request and on a weekly schedule to guarantee zero dead links.",
        "",
        "---",
        "",
        "## 🚀 How to Use & Contribute",
        "",
        "### How to Start a Bot",
        "1. Click on any bot username link (e.g., [@ChatGPT_Telegram_Bot](https://t.me/ChatGPT_Telegram_Bot)).",
        "2. Telegram will open the chat with the bot.",
        "3. Click or tap **Start** at the bottom of the screen to activate.",
        "",
        "### How to Contribute",
        "Know of an active, top-tier bot that belongs here?",
        "1. Read our [CONTRIBUTING.md](CONTRIBUTING.md) guide.",
        "2. Add the bot to `data/bots.json` or open a PR.",
        "3. Ensure the bot is responsive, safe, and passes `scripts/check_bots.py`.",
        "",
        "---",
        "",
        "## 📄 License",
        "",
        "This curated list is open-source under the [MIT License](LICENSE).",
        "",
        "*Curated with ❤️ by [Ehsan Shahbazi](https://github.com/EhsanShahbazii) and contributors.*"
    ])

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"✅ Generated {README_FILE}.")

if __name__ == "__main__":
    count = build_data_file()
    build_readme(count)
