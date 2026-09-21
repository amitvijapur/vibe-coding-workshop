"""Build the editable workshop draft and its softly textured backgrounds."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from reportlab.graphics.barcode import qrencoder
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.xmlchemy import OxmlElement
from pptx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'out'
ASSETS = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
ASSETS.mkdir(exist_ok=True)
W, H = 13.333333, 7.5
INK = '181918'
MUTED = '50504B'
PAPER = 'F2F1EC'
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(W), Inches(H)
prs.core_properties.title = 'Vibe coding | Amit + Jason'
prs.core_properties.subject = 'Workshop review draft'
prs.core_properties.author = 'Amit + Jason'

def gradient(name, base, spots, strength=1):
    width, height = 1920, 1080
    xx, yy = np.meshgrid(np.linspace(0, 1, width), np.linspace(0, 1, height))
    arr = np.ones((height, width, 3)) * np.array(base)
    for cx, cy, rx, ry, color, opacity in spots:
        weight = np.exp(-((xx-cx)**2/rx**2 + (yy-cy)**2/ry**2)*1.75) * opacity * strength
        arr = arr * (1-weight[..., None]) + np.array(color)*weight[..., None]
    noise = np.random.default_rng(41).normal(0, 0.72, (height, width, 1))
    Image.fromarray(np.uint8(np.clip(arr+noise, 0, 255))).save(ASSETS / f'{name}.jpg', quality=94)

gradient('warm', (246, 178, 106), [
    (.12,.14,.68,.95,(248,119,59),.9),(.79,.1,.60,.70,(255,180,216),.98),
    (.57,.84,.66,.67,(237,108,154),.85),(1,.87,.4,.6,(193,186,242),.98)])
gradient('cool', (197,215,242), [
    (.07,.2,.55,.8,(177,198,245),.9),(.77,.15,.63,.8,(204,235,182),.98),
    (.38,.93,.54,.65,(149,194,233),.9),(1,.95,.47,.5,(241,226,144),.9)])
gradient('sun', (247,221,153), [
    (.11,.04,.55,.7,(247,169,111),.9),(.82,.10,.57,.5,(248,232,161),.9),
    (.2,.95,.60,.7,(227,162,199),.9),(.91,.92,.57,.8,(197,211,175),.85)])
gradient('paper', (242,241,236), [
    (1.10,1.18,.63,.60,(241,172,148),.52),(.93,1.20,.4,.4,(216,185,233),.36)])

def textbox(slide, value, x, y, w, h, size=26, color=INK, weight='Regular', spacing=1.06):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.TOP
    for i, line in enumerate(value.split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.name = 'General Sans' if weight == 'Regular' else f'General Sans {weight}'
        p.font.size = Pt(size)
        p.font.color.rgb = RGBColor.from_string(color)
        p.line_spacing = spacing
        p.space_after = Pt(0)
    return box

def line(slide, x, y, width, color='B9B8AF'):
    sh = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(width), Inches(.009))
    sh.fill.solid()
    sh.fill.fore_color.rgb = RGBColor.from_string(color)
    sh.line.fill.background()
    sh._element.spPr.append(OxmlElement('a:effectLst'))
    style = sh._element.find(qn('p:style'))
    if style is not None:
        sh._element.remove(style)

def slide(label, background='paper', note=''):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.shapes.add_picture(str(ASSETS / f'{background}.jpg'), 0, 0, width=prs.slide_width, height=prs.slide_height)
    textbox(s, 'AMIT + JASON', .60, .34, 3, .24, 11, weight='Medium')
    textbox(s, f'{len(prs.slides):02}', 12.18, .34, .5, .24, 11)
    if note:
        s.notes_slide.notes_text_frame.text = note
    return s

def title(s, text, y=1.15, size=49, w=12.0):
    textbox(s, text, .65, .8, w, 1.65, 54, weight='Medium', spacing=1.0)

s = slide('Workshop draft · version 6', 'paper', 'Welcome. Today is for complete beginners. Introduce this as a chance to build one small working thing with AI. Confirm the official event name before adding it. The demonstration venture and its final prompt are still to be chosen by Amit and Jason.')
textbox(s, 'FROM IDEA TO FIRST PROTOTYPE', .63, 1.7, 8, .35, 13)
textbox(s, 'Vibe\ncoding.', .50, 2.47, 12.1, 3.7, 112, weight='Medium', spacing=.90)
textbox(s, 'A workshop with Amit + Jason', .63, 6.59, 9, .4, 20)

s = slide('Your hosts', 'warm', 'Verified against the founder-supplied DragonFly deck, slide-copy.md lines 175–198. Amit Vijapur: CTO, Computer Science at Durham, Accenture software engineering internship, built open-source Cortex. Jason Cheng: CEO, Economics at Durham, Entrepreneur Society President, venture capital, investment banking and startup experience. Introduce yourselves briefly. No workshop-specific claims or additional credentials have been invented.')
title(s, 'About us', 1.08, 53)
for x,filename in [(.40,'amit-cutout.png'),(6.77,'jason-cutout.png')]:
    s.shapes.add_picture(str(ASSETS/'v6'/filename),Inches(x),Inches(2.75),width=Inches(2.70))
textbox(s, 'Amit Vijapur', 3.10, 2.6, 3.47, .8, 31, weight='Medium')
textbox(s, 'Jason Cheng', 9.47, 2.6, 3.24, .8, 31, weight='Medium')
textbox(s, 'CTO, DragonFly\nComputer Science,\nDurham\nAWS SBGL', 3.10, 3.65, 3.47, 2.3, 22, spacing=1.25)
textbox(s, 'CEO, DragonFly\nEconomics, Durham\nEntrepreneur Society\nPresident', 9.47, 3.65, 3.24, 2.3, 22, spacing=1.25)

s = slide('Today’s plan', 'sun', 'Set expectations without inventing a total session length. First we run a live demonstration while teaching two frameworks: a useful prompt and a feedback loop. Next allow 5–10 minutes for questions, then everyone builds a small project for 30–45 minutes. Agree the exact duration and speaking split before the workshop. The demonstration and explanation timings remain flexible.')
title(s, 'Workshop plan', 1.07, 56)
agenda=[('01','Live demo + two frameworks','Build in the background as we learn.'),
        ('02','Questions + discussion','5–10 minutes'),
        ('03','Your own small project','30–45 minutes')]
for i,(n,h,d) in enumerate(agenda):
    y=2.57+i*1.1
    textbox(s,n,.65,y,.7,.4,17)
    textbox(s,h,1.5,y-.04,7.1,.6,29,weight='Medium')
    textbox(s,d,1.5,y+.57,10.8,.5,20)

s = slide('What is vibe coding?', note='Andrej Karpathy coined the term vibe coding in February 2025. He is an AI researcher, former Tesla AI lead and an OpenAI founding member. His original description meant talking to AI, running its output and accepting changes without closely reading every line, especially for throwaway weekend projects. Today we use that approachable workflow and explicitly check what the output does. The beginner message distinguishes a first prototype from a fully reviewed product. Original post: https://x.com/karpathy/status/1886192184808149383 ; corroborating accounts: https://arstechnica.com/ai/2025/03/is-vibe-coding-with-ai-gnarly-or-reckless-maybe-some-of-both/ and https://apnews.com/article/09f35ccc7545ac92447a19565322f13d . Define prompt as an instruction to AI and prototype as a first working version.')
title(s, 'What is vibe coding?')
textbox(s, 'You can build a first prototype\nwithout knowing how to code.', .65, 1.98, 12, 1.21, 33, weight='Medium', spacing=1.08)
textbox(s, 'You describe what you want. AI writes the code.', .65, 3.37, 12, .62, 25)
textbox(s, '“I just see stuff, say stuff, run stuff, and copy paste stuff,\nand it mostly works.”', .65, 4.26, 12, 1.07, 26, spacing=1.12)
textbox(s, 'Andrej Karpathy, AI researcher and former Tesla AI lead.\nHe named it in February 2025: building with AI without reading every line.', .65, 5.60, 12, .92, 19, MUTED, spacing=1.16)
textbox(s, 'You still need to check what it builds.', .65, 6.78, 12, .43, 21)
s.notes_slide.notes_text_frame.text += ' Alternate 19-word quotation verified from the original post transcription at https://threadreaderapp.com/thread/1886192184808149383.html and https://www.figma.com/blog/double-click-vibe-coding/ .'

s = slide('Live demo · start', 'cool', 'LIVE DEMO CUE. The chosen concept helps Durham students compare rentals across websites and find compatible flatmates. Use fictional sample listings and profiles in the demonstration, not live aggregation or real personal information. Finalise the actual build prompt with Jason, show it briefly, and submit it to Codex now. Return to the teaching slides while it runs. The club-event example later is a separate teaching example. Have a saved version available as a clearly labelled backup if the live build is still running.')
title(s, 'Live demo', 1.1, 67)
textbox(s, 'One audience. One problem. One useful action.', .64, 4.15, 12, .9, 29)
line(s,.64,5.37,12.02,'78909D')
textbox(s, 'DEMO CONCEPT', .64, 5.72, 3.0, .3, 12, weight='Medium')
textbox(s, 'A tool that helps Durham students compare rentals across websites and find compatible flatmates.', 3.43, 5.60, 9.24, 1.05, 23)
textbox(s, 'Start the build in Codex. Then return here.', .64, 6.75, 11.8, .3, 14)

s = slide('While it builds · the tools', note='Our suggested tools are ChatGPT or Claude for conversation, Codex or Claude Code as coding agents, and Cursor or Lovable as other options. The marks shown are official brand assets. The OpenAI mark is used for ChatGPT and Codex; the Claude mark is used for Claude and Claude Code. ChatGPT and Claude can help shape the idea and brief. Codex and Claude Code can build, run and improve a project. Codex is used in today’s demo. Cursor puts AI help alongside project files and an editor. Lovable is a browser-based app builder. These capabilities overlap; the suggested roles are not exclusive restrictions. Participants do not need all three tools. Choose the participant tool in advance and check account access, device requirements and initial project setup before the event. No price or access promises are made. Official references: https://help.openai.com/en/articles/12677804-what-is-chatgpt-faq ; https://openai.com/codex/ ; https://cursor.com/ ; https://docs.cursor.com/chat/overview ; https://lovable.dev/ ; https://support.anthropic.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan .')
title(s, 'AI tools', 1.05, 49)

def mini_rect(x,y,w,h,fill,stroke=None):
    sh=s.shapes.add_shape(1,Inches(x),Inches(y),Inches(w),Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb=RGBColor.from_string(fill)
    if stroke:
        sh.line.color.rgb=RGBColor.from_string(stroke)
        sh.line.width=Pt(.7)
    else:
        sh.line.fill.background()
    style=sh._element.find(qn('p:style'))
    if style is not None: sh._element.remove(style)
    sh._element.spPr.append(OxmlElement('a:effectLst'))
    return sh

columns=[
    (.65,[('ChatGPT','openai.png'),('Claude','claude.png')],'Shape your idea and write your brief.','E8C6BE'),
    (4.91,[('Codex','openai.png'),('Claude Code','claude.png')],'Ask AI to build, run and improve your project.','C7D9EB'),
    (9.17,[('Cursor','cursor.png'),('Lovable','lovable.png')],'Build in an AI editor or a browser-based app builder.','D4DEC0')]
for x,products,description,tint in columns:
    mini_rect(x,2.45,3.51,.055,tint)
    for j,(name,logo) in enumerate(products):
        y=2.97+j*1.23
        s.shapes.add_picture(str(ASSETS/'v5'/logo),Inches(x),Inches(y),Inches(.64),Inches(.64))
        textbox(s,name,x+.86,y+.06,2.7,.59,26,weight='Medium')
    textbox(s,description,x,5.40,3.53,1.33,21,spacing=1.13)
textbox(s,'Codex is today’s demo.',4.91,6.68,4.0,.30,12,MUTED)
textbox(s, 'Choose a tool. Use the same two frameworks.', .65, 7.05, 12,.32,18,MUTED)

s = slide('Framework 1 · prompting', 'warm', 'FRAMEWORK 1, prompting. These are the five parts adapted from Ducksss’s source workshop: Purpose, Design, Behaviour, Constraints, Verify. A prompt is simply the instruction you give the tool. Explain each part using the exact demo prompt while Codex works. Design includes simple visual references. Behaviour means what happens after an action. Constraints keep the first version small. Verify means naming what you will personally check.')
title(s, 'What makes up a good prompt', .97, 49)
items = [('Purpose','Who is it for? What should it help them do?'),('Design','What should it look and feel like?'),('Behaviour','What happens when someone uses it?'),('Constraints','What belongs in this first version?'),('Verify','What must work for us to call it done?')]
for i,(head,question) in enumerate(items):
    y=2.47+i*.76
    textbox(s,f'0{i+1}',.66,y,.75,.45,17)
    textbox(s,head,1.55,y-.04,3.0,.52,30,weight='Medium')
    textbox(s,question,5.00,y+.01,7.6,.5,21)

s = slide('Framework 1 · a small example', note='This miniature club-event example is for learning; it is not the chosen live venture demonstration. Purpose: students need to find the next club event. Design: simple, readable phone layout. Behaviour: opening the details reveals the time and location. Constraints: one page with fictional details and no login. Verify: the button opens the correct details and the page works on a narrow screen. Point to each sentence and match it to the framework. A fuller real brief can be longer.')
title(s, 'Prompt example')
textbox(s, 'PRETEND CODEX CONVERSATION · TEACHING EXAMPLE', .65, 2.10, 12, .35, 12, MUTED)
mini_rect(.65,2.48,12.03,3.92,'FAF9F5','D4D4CC')
textbox(s,'Codex',.98,2.63,3.0,.4,20,weight='Medium')
line(s,.98,3.15,11.35,'D4D4CC')
textbox(s,'You',.98,3.28,1.5,.3,13,weight='Medium')
box=s.shapes.add_textbox(Inches(.98),Inches(3.71),Inches(11.34),Inches(2.19))
tf=box.text_frame
tf.word_wrap=True
tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
p=tf.paragraphs[0]
p.line_spacing=1.32
segments=[
    ('Purpose','Hey, I want to make an app that helps students find our next club event. ','EAC5BA'),
    ('Design','Make it easy to read on a phone. ','EBDFA9'),
    ('Behaviour','When I tap “View details”, show me when and where it is. ','CBDECA'),
    ('Constraints','Just one page for now, with made-up details and no login. ','C5D9EB'),
    ('Verify','Check that the right details appear and it works on my phone.','DCCDEC')]
for label,words,color in segments:
    run=p.add_run()
    run.text=words
    run.font.name='General Sans'
    run.font.size=Pt(24)
    run.font.color.rgb=RGBColor.from_string(INK)
    hi=OxmlElement('a:highlight')
    rgb=OxmlElement('a:srgbClr')
    rgb.set('val',color)
    hi.append(rgb)
    run._r.get_or_add_rPr().append(hi)
mini_rect(.98,5.97,11.34,.31,'EEEDE7')
textbox(s,'Ask a follow-up…',1.12,6.0,9.8,.24,12,MUTED)
textbox(s,'↑',11.85,5.96,.29,.30,16)
for i,(label,words,color) in enumerate(segments):
    x=.65+i*2.43
    mini_rect(x,6.82,.22,.22,color)
    textbox(s,label,x+.35,6.73,2.03,.51,19)

s = slide('Framework 2 · iteration + feedback', 'cool', 'FRAMEWORK 2, iteration plus feedback. Define iteration as improving the first version through another round. Check what actually happens, describe a precise improvement, let the tool change it, recheck the result, and save a known working version. The next slide gives the message structure inside Describe; it is not a third framework. A checkpoint is a saved working version. Demonstrate the selected tool’s save/version feature rather than assuming beginners understand Git.')
title(s, 'How to iterate\nand give feedback', 1.04, 49)
steps=[('01','Check','Try the action.'),('02','Describe','Explain the change.'),('03','Change','Let AI update it.'),('04','Recheck','Try it again.'),('05','Save','Keep what works.')]
for i,(num,head,desc) in enumerate(steps):
    y=2.75+i*.66
    textbox(s,num,.65,y,.7,.45,20)
    textbox(s,head,1.6,y-.035,3.3,.57,29,weight='Medium')
    textbox(s,desc,5.25,y+.01,7.2,.54,25)
line(s,.65,6.35,12.0,'78909D')
textbox(s,'Checkpoint = a saved working version.',.65,6.64,12,.5,22)

s = slide('Framework 2 · describe the change', 'sun', 'This four-part feedback message sits inside Describe in Framework 2. It is not an additional framework. Say what happened, what you expected, what should stay unchanged and how to check the update. Use the example only if it describes a real observation or explain that it is a hypothetical teaching example. Here the event button should reveal time and location, which connects back to the sample prompt.')
title(s, 'How to give feedback', 1.06, 48)
feedback=[('What happened','“View details” does nothing.'),
          ('What I expected','Show the event time and location.'),
          ('What to keep','Keep the current page design.'),
          ('How to check','Click the button and check the details.')]
for i,(label,body) in enumerate(feedback):
    y=2.61+i*.79
    textbox(s,label,.65,y,3.6,.5,21,weight='Medium')
    textbox(s,body,4.8,y-.03,7.85,.71,27)
textbox(s,'Then recheck the result yourself.',.65,6.59,12,.5,22)

s = slide('Feedback example', 'paper', 'This is an illustrative follow-up message to the sample event-app prompt, not a report about the live venture demo. Read it in a natural voice. Match the highlighted parts to what happened, expected behaviour, what to keep and how to check. The feedback structure is part of Framework 2, not a third framework.')
title(s,'Feedback example')
textbox(s, 'PRETEND CODEX CONVERSATION · TEACHING EXAMPLE', .65, 2.10, 12, .35, 12, MUTED)
mini_rect(.65,2.48,12.03,3.92,'FAF9F5','D4D4CC')
textbox(s,'Codex',.98,2.63,3.0,.4,20,weight='Medium')
line(s,.98,3.15,11.35,'D4D4CC')
textbox(s,'You',.98,3.28,1.5,.3,13,weight='Medium')
box=s.shapes.add_textbox(Inches(.98),Inches(3.71),Inches(11.34),Inches(2.19))
tf=box.text_frame
tf.word_wrap=True
tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
p=tf.paragraphs[0]
p.line_spacing=1.32
feedback_segments=[
    ('What happened','Hey, I tapped “View details” but nothing happened. ','EAC5BA'),
    ('Expected','I expected it to show the event time and location. ','EBDFA9'),
    ('Keep','Please fix that but keep the page looking the same. ','C5D9EB'),
    ('Check','Then try the button and check that the correct details show up.','DCCDEC')]
for label,words,color in feedback_segments:
    run=p.add_run()
    run.text=words
    run.font.name='General Sans'
    run.font.size=Pt(24)
    run.font.color.rgb=RGBColor.from_string(INK)
    hi=OxmlElement('a:highlight')
    rgb=OxmlElement('a:srgbClr')
    rgb.set('val',color)
    hi.append(rgb)
    run._r.get_or_add_rPr().append(hi)
mini_rect(.98,5.97,11.34,.31,'EEEDE7')
textbox(s,'Ask a follow-up…',1.12,6.0,9.8,.24,12,MUTED)
textbox(s,'↑',11.85,5.96,.29,.30,16)
for i,(label,words,color) in enumerate(feedback_segments):
    x=.65+i*3.09
    mini_rect(x,6.82,.22,.22,color)
    textbox(s,label,x+.35,6.73,2.67,.51,19)

s = slide('Live demo · review', 'cool', 'Switch back to Codex. Show its status and a brief summary of the work. If the build is ready, show the result and compare it with the original brief. Ask what was requested and what the room can observe. If it is still running, say so. Use a saved version only if labelled as prepared earlier; do not claim it was generated live. The next slide gives concrete checks for complete beginners.')
title(s, 'Review the demo', 1.03, 79)
textbox(s, 'What did we ask for?\nWhat did we get?', .65, 4.39, 12, 1.7, 35, spacing=1.2)

s = slide('Live demo · check', note='Briefly distinguish Codex’s report from observed evidence. A summary saying a feature works is not the same as seeing it work. Run the main action, try missing or wrong input when the app has inputs, and check a narrow phone layout. If there are no inputs, choose a relevant alternate state instead. These are suggested checks, not claims of passed tests. Use fictional information only. Review further before collecting personal data, accepting payments or serving real users.')
title(s, 'Check the result', 1.05, 50)
checks=[('01','The main action','Does the button or action actually work?'),
        ('02','Missing or wrong input','What happens if a field is empty?'),
        ('03','A phone-sized screen','Can you still read and use it?')]
for i,(n,h,d) in enumerate(checks):
    y=2.48+i*1.04
    textbox(s,n,.65,y,.7,.4,17,MUTED)
    textbox(s,h,1.52,y-.04,4.7,.74,27,weight='Medium')
    textbox(s,d,6.37,y+.03,6.1,.9,23)
line(s,.65,6.01,12.0)
textbox(s, 'Use fictional data. Review before real users or payments.', .65, 6.49, 12,.55,20,MUTED)

s = slide('Live demo · complete the loop', 'sun', 'Demonstrate Framework 2 once. Find one genuine mismatch or choose one small audience-requested improvement, describe it using the four message parts, let Codex make the change, recheck it and save. If the original version has no clear bug, intentionally make a small useful improvement. Do not invent a failure. Ensure the room sees how the follow-up relates to their first prompt.')
title(s, 'Make one improvement', 1.07, 57)
rows=['Check what could be better.','Describe one focused change.','Let AI update it.','Recheck. Save the working version.']
for i,r in enumerate(rows):
    textbox(s,f'0{i+1}',.66,2.82+i*.77,.7,.4,17)
    textbox(s,r,1.58,2.76+i*.77,10.6,.65,30)

s = slide('Questions + discussion', 'warm', 'Allow 5–10 minutes for questions and discussion immediately after the demonstration, before the participant build. Invite questions about the tools and two frameworks, then introduce the 30–45 minute project activity. Be clear that their result is a prototype, and encourage further checking before real use. Pending review decisions: official event title, venture demo and prompt, presenter ownership, participant tool/account setup and final activity duration. Source teaching material adapted from Chai Pin Zheng (Ducksss), https://github.com/Ducksss/vibe-coding-workshop. Visual direction inspired by Orange by Marmalade 2025, Marmalade Collective, via https://www.deck.gallery/orange-by-marmalade-2025/.')
title(s, 'Q&A', 1.19, 75)
textbox(s, 'Questions & discussion · 5–10 minutes', .65, 4.83, 12,.8,28)
textbox(s, 'Teaching material adapted from Chai Pin Zheng (Ducksss) · github.com/Ducksss/vibe-coding-workshop\nVisual reference: Orange by Marmalade 2025 · Marmalade Collective via Deck Gallery', .65, 6.55, 12.0,.60,11,spacing=1.3)


s = slide('Your turn · a small project', 'warm', 'Participants now build their own small project for 30–45 minutes. The four ideas are venture concepts, but the workshop scope is one working interaction with fictional data. For the food idea, browse a few sample meals and reserve one. For freelance work, browse services and request one. For sponsor matching, show sample matches and an interest request. For local services, compare a few fictional quotes. Do not build full marketplaces, payments, real messaging, fulfilment or matching infrastructure. Use fictional data and avoid payments or login. Before the event, agree the participant tool and make sure it is accessible. Amit and Jason circulate and help. A saved project is sufficient; no public deployment is required.')
title(s, 'Build your own project', 1.04, 49)
textbox(s,'30–45 MINUTES',.65,2.27,12,.4,14,weight='Medium')
ideas=[
    ('Surplus-food marketplace','Browse sample meals and show a reservation.'),
    ('Student freelance marketplace','Browse services and preview a request.'),
    ('Creator–sponsor matching','Browse sample matches and preview a pitch.'),
    ('Local service quote platform','Compare sample quotes for a job.')]
for i,(idea,scope) in enumerate(ideas):
    y=2.87+i*.83
    textbox(s,idea,.65,y,6.2,.55,25,weight='Medium')
    textbox(s,scope,7.15,y+.04,5.53,.68,21)
line(s,.65,6.38,12)
textbox(s,'Build one interaction with made-up data. Improve it once. Check it.',.65,6.74,12,.48,20)

s = slide('Your turn · use the time', note='The core schedule totals exactly 30 minutes: 5 to choose an idea and write the brief, 15 for the first build, 7 to improve and check, and 3 to save a working version. If allocated 45 minutes, use the extra 15 to refine and review with a partner. Ask partners to try the key interaction and give one concrete observation. Stop adding features in the final few minutes and preserve a working result. These timings apply only to the participant activity, not the whole workshop.')
title(s, 'Project schedule', 1.05, 53)
schedule=[('5 min','Choose an idea + write your brief.'),
          ('15 min','Build the first version.'),
          ('7 min','Improve it + check it.'),
          ('3 min','Save your working version.')]
for i,(time,action) in enumerate(schedule):
    y=2.54+i*.81
    textbox(s,time,.65,y,2.2,.6,28,weight='Medium')
    textbox(s,action,3.38,y,9.2,.65,28)
line(s,.65,6.06,12)
textbox(s,'Have 45 minutes? Add 15 to refine and review with a partner.',.65,6.43,12,.65,21)

s = slide('Two frameworks to keep', 'cool', 'Use this as the final reminder as participants wrap up, or leave it on screen during the activity if useful. There are exactly two frameworks: the five-part brief for the initial prompt, and the iteration-plus-feedback loop for improvement. The four-part feedback message is inside Describe in the second framework. Encourage participants to save this slide or their notes.')
title(s, 'Two frameworks', 1.05, 46)
textbox(s,'01',.65,2.69,1,.5,18)
textbox(s,'How to prompt',1.61,2.62,10.4,.7,35,weight='Medium')
textbox(s,'Purpose · Design · Behaviour\nConstraints · Verify',1.61,3.58,10.7,1.15,25,spacing=1.22)
textbox(s,'02',.65,5.01,1,.5,18)
textbox(s,'How to iterate and feedback',1.61,4.94,10.4,.7,35,weight='Medium')
textbox(s,'Check · Describe · Change · Recheck · Save',1.61,5.94,11.0,.78,24)


s = slide('Connect with us', 'cool', 'Amit LinkedIn verified from the founder-profile source: https://www.linkedin.com/in/amitvijapur/ . Jason LinkedIn supplied directly by the user: https://www.linkedin.com/in/jasoncty/ . The QR codes encode these exact HTTPS URLs and the visible handles are clickable hyperlinks.')
title(s,'Connect with us')
for x,name,handle in [(.65,'Amit Vijapur','amitvijapur'),(7.10,'Jason Cheng','jasoncty')]:
    url=f'https://www.linkedin.com/in/{handle}/'
    textbox(s,name,x,2.48,5.5,.8,36,weight='Medium')
    qr=qrencoder.QRCode(None,1)
    qr.addData(url)
    qr.make()
    count=qr.getModuleCount()
    scale=12
    qim=Image.new('RGB',((count+8)*scale,(count+8)*scale),'white')
    draw=ImageDraw.Draw(qim)
    for row in range(count):
        for col in range(count):
            if qr.isDark(row,col):
                draw.rectangle(((col+4)*scale,(row+4)*scale,(col+5)*scale-1,(row+5)*scale-1),fill='black')
    qpath=OUT/f'v6-qr-{handle}.png'
    qim.save(qpath)
    pic=s.shapes.add_picture(str(qpath),Inches(x),Inches(3.54),width=Inches(2.25))
    pic.click_action.hyperlink.address=url
    link=textbox(s,f'linkedin.com/in/{handle}',x,6.08,5.48,.62,22)
    link.text_frame.paragraphs[0].runs[0].hyperlink.address=url

s = slide('Thank you', 'warm', 'Thank everyone for participating. Encourage them to keep their first working version and return to the two frameworks when improving it.')
title(s,'Thank you')
textbox(s,'Amit + Jason',.65,5.95,12,.8,32)


destination=OUT/'vibe-coding-workshop-draft-v8.pptx'
prs.save(destination)
print(destination)
print(f'{len(prs.slides)} slides; native editable text; presenter notes on every slide.')
