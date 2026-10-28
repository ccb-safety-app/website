"""The how-to guides, one per add-on, written as data.

  python3 howto.py      (build.py runs it too)

Writes src/guides/how-to-use-<app>.html. Each step has: what to do, a screenshot, and
"If it doesn't work" fixes. Edit the text here, not the generated pages.
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).parent

ONE_ACCOUNT = ("<b>The panel says \"Signed in to more than one Google account?\"</b> Google add-ons can mix up accounts when "
               "several are signed in to the same browser. Open the file in a private window signed in to only one account, "
               "or sign out of the others, then open the add-on again.")

APPS = [
    {
        "slug": "label-maker", "name": "Spreadsheet Labels", "where": "Google Sheets", "minutes": "5 minutes",
        "plan": "Free for documents up to 3 pages",
        "lede": "Turn a list of names and addresses in a Google Sheet into print-ready Avery labels or envelopes. Here's every step, with what to do if something looks off.",
        "steps": [
            {"title": "Open Spreadsheet Labels beside your sheet", "img": "label-maker-open.png", "wide": True,
             "alt": "A Google Sheet of addresses with Spreadsheet Labels open on the right.",
             "text": "Open the Google Sheet with your addresses. Put one person per row, with headings in the first row such as First Name, Last Name, Address 1, City, State and Zip.",
             "do": ["Click <b>Extensions</b> in the menu bar.", "Choose <b>Spreadsheet Labels</b>, then <b>Open</b>.", "No sheet yet? Choose <b>Add a Sample Sheet</b> to try it with example addresses."],
             "fix": [ONE_ACCOUNT,
                     "<b>Spreadsheet Labels isn't in the Extensions menu.</b> Reload the sheet. If it's still missing, install it again from the Google Workspace Marketplace."]},
            {"title": "Choose your label sheet", "img": "label-maker-sheet.png",
             "alt": "Step 1 in Spreadsheet Labels: a list of Avery label sheets with Avery 5160 selected.",
             "text": "Find the product number on your box of labels, such as 5160 or 8160, and pick it from the list.",
             "do": ["Type the number in <b>Find your label sheet</b>.", "Click the matching sheet. The tick shows it's chosen.", "Can't find yours? Choose <b>Show all sizes</b>, or <b>Add your own size</b> and type the measurements from the box."],
             "fix": ["<b>My number isn't listed.</b> Many numbers share one layout: 8160, 5260 and 18160 all print like 5160. The box usually says \"Use template 5160\"."]},
            {"title": "Arrange the text", "img": "label-maker-arrange.png",
             "alt": "Step 2 in Spreadsheet Labels: column chips for each line of the label.",
             "text": "Spreadsheet Labels reads the headings in your sheet and suggests a layout. Each line of the label is a row of column chips.",
             "do": ["Drag a column onto a line to add it, or click the <b>×</b> on a chip to remove it.", "Use <b>Paste a list</b> to paste addresses from anywhere, or <b>Type addresses</b> to type a few.", "Use <b>One label</b> to print the same label many times, such as a return address."],
             "fix": ["<b>\"Could not read your sheet.\"</b> Click <b>Try again</b>. If it keeps happening, close the panel and open it again from the Extensions menu.",
                     "<b>The wrong row is used as headings.</b> Put your headings in row 1, or choose <b>No heading row</b> in the panel."]},
            {"title": "Preview and check addresses", "img": "label-maker-check.png",
             "alt": "Check addresses in Spreadsheet Labels, suggesting corrected street names and zip codes.",
             "text": "The preview shows a real label from your sheet. Use the arrows to look through rows. Before printing a big batch, let Spreadsheet Labels check the addresses for typos.",
             "do": ["Click <b>Check addresses</b>.", "Review each suggestion and choose <b>Accept</b> or <b>Keep mine</b>.", "Choose <b>Accept all</b> if the suggestions look right."],
             "fix": ["<b>An address can't be found.</b> It may be new or rural. Check it by hand, then choose <b>Keep mine</b>. It will still print."]},
            {"title": "Choose rows, copies and style", "img": "label-maker-preview.png",
             "alt": "Spreadsheet Labels options: rows to print, copies, text style, pictures and codes.",
             "text": "Print every row, only the rows you've selected, or a range. You can also print copies, change the font and size, and add a QR code, barcode or picture to each label.",
             "do": ["Open <b>Rows to print</b> to pick which rows.", "Open <b>Copies</b> to print each label more than once.", "Open <b>Text style</b> to change the font, size or alignment.", "Open <b>Pictures and codes</b> to add a logo, QR code or barcode."],
             "fix": ["<b>Text is cut off on a label.</b> Choose a smaller size in <b>Text style</b>, or turn on automatic size. Long lines shrink to fit."]},
            {"title": "Line up your printer once", "img": "label-maker-alignment.png",
             "alt": "Spreadsheet Labels' start position and printer alignment settings.",
             "text": "Every printer feeds a little differently. Print one test page on plain paper, hold it against a label sheet up to the light, and nudge the layout if needed. Spreadsheet Labels remembers it.",
             "do": ["Click <b>Print a test page</b>.", "If labels sit too high, low, left or right, open <b>Printer alignment</b> and move them in small steps.", "Using a sheet you've partly used? Set <b>Start position</b> to the first empty label."],
             "fix": ["<b>Everything is slightly too small or too big.</b> In your printer window, set Scale to <b>100%</b> or <b>Actual size</b>, not \"Fit to page\".",
                     "<b>Labels drift lower down the page.</b> Check the paper size is Letter (or A4 for A4 sheets) in the print window."]},
            {"title": "Create and print your labels", "img": "label-maker-ready.png",
             "alt": "Spreadsheet Labels after creating labels: Download PDF and Open document buttons.",
             "text": "Spreadsheet Labels builds a Google Doc with your labels. Download it as a PDF and print at 100%.",
             "do": ["Click <b>Create labels</b>.", "Click <b>Download PDF</b> and print at 100%, or <b>Open document</b> to edit any label first."],
             "fix": ["<b>\"The labels could not be created.\"</b> Google sometimes has a short hiccup. Click <b>Try again</b>.",
                     "<b>It stops at 3 pages.</b> The free plan makes documents of up to 3 pages (90 Avery 5160 labels). Pro has no page limit."]},
        ],
    },
    {
        "slug": "certificate-maker", "name": "Certificate Maker", "where": "Google Sheets", "minutes": "5 minutes",
        "plan": "Free for 5 certificates a month",
        "lede": "Make a personalized certificate for everyone on a Google Sheet, then save them to Drive or email each person theirs. The panel walks you through five steps.",
        "steps": [
            {"title": "Put your names in a sheet and open the add-on", "img": "certificate-maker-design.png",
             "alt": "Certificate Maker open beside a sheet, showing a live certificate preview.",
             "text": "Use one row per person, with columns such as Name, Email and Course. A Google Form's response sheet works too.",
             "do": ["Click <b>Extensions</b>, then <b>Certificate Maker</b>, then <b>Open Certificate Maker</b>.", "The preview at the top shows a real certificate for the first row. Use the arrows to see other people.", "No sheet yet? Choose <b>Add a Sample Sheet</b>."],
             "fix": [ONE_ACCOUNT]},
            {"title": "Pick a design", "img": "certificate-maker-design.png", "crop": "low",
             "alt": "The Design step: a category list and a gallery of certificate designs.",
             "text": "Pick a category, then a design. Choose a color and the paper size (US Letter or A4).",
             "do": ["Choose a <b>Category</b>, such as Completion or Achievement & Award.", "Click a design in the gallery.", "Pick a <b>Color</b> and <b>Paper</b> size."],
             "fix": []},
            {"title": "Use your own Google Slides design (optional)", "img": "certificate-maker-own-design.png",
             "alt": "The My Slides Design tab with a Choose from Google Drive link.",
             "text": "Already have a certificate in Google Slides? Type placeholders like <code>{{Name}}</code> and <code>{{Course}}</code> where the details go, then choose it here.",
             "do": ["Click <b>My Slides Design</b>.", "Click <b>Choose from Google Drive</b> and pick your presentation.", "The panel lists the placeholders it found."],
             "fix": ["<b>\"That presentation could not be opened.\"</b> Choose it with <b>Choose from Google Drive</b> rather than pasting the link. That gives Certificate Maker permission to open that one file.",
                     "<b>No placeholders found.</b> Type them with double curly brackets, exactly like <code>{{Name}}</code>, in a text box on the first slide."]},
            {"title": "Fill in the details", "img": "certificate-maker-details.png",
             "alt": "The Details step: sheet, course, date, organization and title settings.",
             "text": "Tell Certificate Maker which column holds each detail, or type text that's the same for everyone.",
             "do": ["Pick the <b>Sheet</b> with your names.", "For each detail, choose a column or type the text.", "Set the <b>Date</b>: today, a fixed date, or a column."],
             "fix": []},
            {"title": "Check the names", "img": "certificate-maker-name-check.png",
             "alt": "The Name Check step with capital letter fixes and long names.",
             "text": "Certificate Maker looks for names typed in all capitals or all lower case, and names too long for the line.",
             "do": ["Choose <b>Fix Them</b> to correct capital letters, such as <i>maria lopez</i> to <i>Maria Lopez</i>.", "Long names shrink to fit. Check the ones listed."],
             "fix": []},
            {"title": "Add your logo and signatures", "img": "certificate-maker-logo.png",
             "alt": "The Logo and Signatures step: signer name, title and a signature pad.",
             "text": "Add up to three signers. Each has a name, a title and a signature you draw or upload. You can also add a logo and a seal.",
             "do": ["Type the signer's <b>Name</b> and <b>Title</b>.", "Draw the signature, or upload a photo of it. Turn on <b>Remove Background</b> to drop the paper color.", "Click <b>Upload</b> under Logo to add your logo."],
             "fix": ["<b>The signature has a gray box around it.</b> Turn on <b>Remove Background</b>, or upload a PNG with a clear background."]},
            {"title": "Choose delivery and make them", "img": "certificate-maker-delivery.png",
             "alt": "The Delivery step: email, QR code, numbering, one combined PDF and file names.",
             "text": "Choose what happens to each certificate. They're always saved as PDFs in your Drive.",
             "do": ["Turn on <b>Email Each Person Their Certificate</b> to send them out.", "Keep <b>QR Code to Check It's Genuine</b> on, so anyone can confirm a certificate is real.", "Turn on <b>Number Each Certificate</b> for an ID like CERT-2026-0001.", "Click <b>Preview</b> to see exactly how the first one looks, then <b>Create Certificates</b>."],
             "fix": ["<b>\"Free Left This Month: 0\".</b> The free plan makes 5 certificates a month. They come back on the 1st, or Pro makes unlimited certificates.",
                     "<b>Emails stopped partway.</b> Google limits how many emails an account can send each day. The rest are sent when you run it again tomorrow.",
                     "<b>\"Couldn't Save to Drive\".</b> Google had a short problem. Wait a minute and click Create Certificates again. Finished ones aren't made twice."]},
        ],
    },
    {
        "slug": "form-limits", "name": "Form Limits", "where": "Google Forms", "minutes": "3 minutes",
        "plan": "Free on one form at a time",
        "lede": "Give each choice in your Google Form a number of places, close the form after a number of responses or at a set time, and keep a real waitlist.",
        "steps": [
            {"title": "Open Form Limits in your form", "img": "form-limits-start.png",
             "alt": "Form Limits open beside a form, with limits switched off.",
             "text": "Open your form in edit mode. It needs at least one multiple-choice, dropdown or checkbox question for choice limits.",
             "do": ["Click the <b>puzzle piece</b> (Add-ons) at the top of the form.", "Choose <b>Form Limits</b>, then <b>Open Form Limits</b>."],
             "fix": [ONE_ACCOUNT]},
            {"title": "Set places for each choice", "img": "form-limits-choices.png",
             "alt": "Choice Limits: places per session with full and waiting counts.",
             "text": "Pick a question, then give every choice the same number of places, or a number for each choice.",
             "do": ["Open <b>Choice Limits</b>.", "Choose <b>Same for All</b> or <b>Each Choice</b> and type the number of places.", "Under <b>When a Choice Is Full</b>, choose <b>Remove It</b> or <b>Offer a Waitlist</b>.", "Keep <b>Show Places Left</b> on so people see \"(3 left)\"."],
             "fix": ["<b>My question isn't listed.</b> Choice limits work on multiple-choice, dropdown and checkbox questions."]},
            {"title": "Close after a number of responses (optional)", "img": "form-limits-response-limit.png",
             "alt": "Response Limit: close after 40 responses.",
             "text": "Stop the whole form once it has enough responses, such as 40 seats in a room.",
             "do": ["Open <b>Response Limit</b> and turn on <b>Close After a Number of Responses</b>.", "Type the number."],
             "fix": []},
            {"title": "Open and close at set times (optional)", "img": "form-limits-times.png",
             "alt": "Open and Close Times with a closing date and weekly opening hours.",
             "text": "Open the form at a set time, close it at another, or keep weekly hours, like office hours that start fresh each week.",
             "do": ["Open <b>Open and Close Times</b>.", "Turn on <b>Open at a Set Time</b> and/or <b>Close at a Set Time</b> and pick the date and time.", "For a weekly routine, turn on <b>Weekly Opening Hours</b>."],
             "fix": ["<b>\"The closing time is in the past.\"</b> Pick a later time, or switch Close at a Set Time off.",
                     "<b>Times are an hour off.</b> Times use the time zone shown under the settings. Check your computer's time zone."]},
            {"title": "Write the closed message", "img": "form-limits-closed.png",
             "alt": "When the Form Is Closed: messages shown when full and before it opens.",
             "text": "Choose what people see when the form is full or not open yet.",
             "do": ["Open <b>When the Form Is Closed</b>.", "Edit the message for when it's full, and the one shown before it opens."],
             "fix": []},
            {"title": "Choose your emails", "img": "form-limits-emails.png",
             "alt": "Emails: alerts to the owner and waitlist emails.",
             "text": "Get an email when the form closes, when a choice fills or when it's 80% full. Waitlisted people can be emailed when a place opens up.",
             "do": ["Open <b>Emails</b> and switch on the ones you want.", "For waitlist emails, pick the question that asks for their email address."],
             "fix": ["<b>Waitlisted people aren't emailed.</b> Turn on <b>Collect email addresses</b> in the form's Settings, or add a short-answer email question and choose it here."]},
            {"title": "Switch limits on and share", "img": "form-limits-share.png",
             "alt": "Share: the form link, a QR code and a Download PNG button.",
             "text": "Save, then share your form. Form Limits keeps it up to date as responses come in.",
             "do": ["Click <b>Switch Limits On</b> (or <b>Save and Apply</b> after changes).", "Open <b>Share</b> for the link and a QR code for posters.", "<b>Activity</b> lists what happened, such as \"Sat 9:00 AM filled up\"."],
             "fix": ["<b>A full choice still shows.</b> The form updates a moment after each response. Reload the form to see it.",
                     "<b>I want the form back to normal.</b> Click <b>Switch Limits Off</b>. Your choices return to how they were."]},
        ],
    },
    {
        "slug": "form-payments", "name": "Form Payments", "where": "Google Forms", "minutes": "10 minutes",
        "plan": "10 payment requests a month",
        "lede": "Ask for payment with every Google Form response. Each person gets an email with an itemized total and buttons to pay by card or PayPal, and you see who's paid.",
        "steps": [
            {"title": "Open Form Payments in your form", "img": "form-payments-track.png",
             "alt": "Form Payments open beside a form, showing money collected and who is waiting.",
             "text": "Open your form in edit mode. Your form needs a way to know each person's email: turn on <b>Collect email addresses</b> in the form's Settings, or ask for it in a question.",
             "do": ["Click the <b>puzzle piece</b> (Add-ons) at the top of the form.", "Choose <b>Form Payments</b>, then <b>Open Form Payments</b>.", "Go to the <b>Setup</b> tab."],
             "fix": [ONE_ACCOUNT]},
            {"title": "Connect how you get paid", "img": "form-payments-connect.png",
             "alt": "Step 1: Stripe and PayPal connected, and Other Ways to Pay.",
             "text": "Money goes straight to your own Stripe or PayPal account. Form Payments never takes a cut.",
             "do": ["<b>Stripe:</b> create a restricted key in your Stripe dashboard with write access to Products, Prices and Payment Links and read access to Checkout Sessions, then paste it.", "<b>PayPal:</b> paste your PayPal app's Client ID and Secret.", "<b>Other Ways to Pay</b> (optional): add your Cash App, Venmo or Zelle details, or say \"pay at the door\"."],
             "fix": ["<b>\"Couldn't Reach Stripe\".</b> Check the key has the permissions above, and that it's a live key (rk_live…) if you want real payments. Test keys (rk_test…) only take test cards."]},
            {"title": "Set your prices", "img": "form-payments-prices.png",
             "alt": "Step 2: a price for each choice, a quantity question and add-ons.",
             "text": "Prices come from the answers: a price for each choice, multiplied by a quantity question if you have one.",
             "do": ["Pick the question and type a price next to each choice.", "Optional: <b>Everyone Pays a Fixed Amount</b>, <b>Quantity From</b> a question, add-ons, or <b>Let People Choose the Amount</b> for donations."],
             "fix": ["<b>A question isn't listed.</b> Prices work with multiple-choice, checkbox, dropdown, scale and short-answer (number) questions."]},
            {"title": "Tax, fees and discount codes (optional)", "img": "form-payments-fees.png",
             "alt": "Step 3: tax, card fee passed on and discount codes.",
             "text": "Add tax, pass the card fee on to the payer, or create discount codes with limits.",
             "do": ["Turn on <b>Add Tax</b> and type the rate.", "Turn on <b>Payer Covers the Card Fee</b> if you want.", "Under <b>Discount Codes</b>, pick the question with the code and add codes."],
             "fix": []},
            {"title": "Write the emails", "img": "form-payments-emails.png",
             "alt": "Step 4: sender name, subject, message, reminders and receipts.",
             "text": "Each person gets a payment request with an itemized total. Unpaid people can get gentle reminders, and everyone gets a receipt when they pay.",
             "do": ["Set the <b>Sender Name</b>, <b>Replies Go To</b> and <b>Subject</b>.", "Edit the message. Tags like <b>Name</b> and <b>Total</b> are filled in for each person.", "Click <b>Send Me a Test</b> to see it in your inbox.", "Turn on <b>Remind People Who Haven't Paid</b> and choose how often."],
             "fix": ["<b>Emails aren't arriving.</b> Check the person's spam folder, and that your form collects email addresses."]},
            {"title": "Show prices on the form", "img": "form-payments-on-form.png",
             "alt": "Step 5: show prices under priced questions and tell people to check their email.",
             "text": "Let people see prices while they fill in the form, and tell them to watch for the payment email.",
             "do": ["Turn on <b>Show Prices Under Priced Questions</b>.", "Keep <b>Tell People to Check Their Email</b> on.", "Click <b>Save Changes</b>."],
             "fix": []},
            {"title": "See who's paid", "img": "form-payments-track.png",
             "alt": "The Payments tab: amount collected, waiting and paid lists.",
             "text": "The <b>Payments</b> tab shows what's been collected and who's still waiting. Everything is also kept in a spreadsheet called <b>Payments: (your form)</b> in your Drive.",
             "do": ["Click <b>Check Now</b> to look for new payments. Form Payments also checks every hour.", "Paid in cash or check? Open the person and choose <b>Mark as Paid</b>. They get a receipt.", "Click <b>Open Sheet</b> for the full record."],
             "fix": ["<b>Someone paid but still shows as waiting.</b> Click <b>Check Now</b>. Card payments can take a minute to show.",
                     "<b>I need to stop one request.</b> Open it and choose <b>Cancel Request</b>. Its payment links stop working."]},
        ],
    },
]

PAGE = """title: How to use {name} for {where}: step-by-step guide | Northpine Apps
description: {desc}
active: guides
heading: How to use {name}
---
<main class="howto">
<section class="howto-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{{{{guides}}}}">Guides</a><span aria-hidden="true">/</span><span>{name}</span></nav>
    <div class="howto-title">
      <img src="{{{{assets}}}}apps/icons/{slug}.svg" width="64" height="64" alt="">
      <div>
        <h1>How to use {name}</h1>
        <p class="lede">{lede}</p>
      </div>
    </div>
    <ul class="facts">
      <li><span>Works in</span><b>{where}</b></li>
      <li><span>Set-up time</span><b>About {minutes}</b></li>
      <li><span>Free plan</span><b>{plan}</b></li>
    </ul>
  </div>
</section>
<div class="wrap howto-grid">
  <nav class="toc" aria-label="Steps">
    <p class="toc-head">On this page</p>
    <ol>
{toc}
      <li class="toc-extra"><a href="#help">Still stuck?</a></li>
    </ol>
  </nav>
  <div class="howto-steps">
{steps}
    <section class="help" id="help">
      <h2>Still stuck?</h2>
      <p>Email <a href="mailto:{{{{EMAIL}}}}">{{{{EMAIL}}}}</a> with a screenshot of the panel and what you expected to happen. We usually reply within a day.</p>
      <p class="help-links"><a href="{{{{app:{slug}}}}}">About {name}</a><a href="{{{{support}}}}">Support</a><a href="{{{{guides}}}}">All guides</a></p>
    </section>
  </div>
</div>
</main>
<script>
(function () {{
  var links = [].slice.call(document.querySelectorAll('.toc a'));
  var map = {{}};
  links.forEach(function (a) {{ map[a.getAttribute('href').slice(1)] = a; }});
  if (!('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (es) {{
    es.forEach(function (e) {{
      if (!e.isIntersecting) return;
      links.forEach(function (a) {{ a.removeAttribute('aria-current'); }});
      var a = map[e.target.id]; if (a) a.setAttribute('aria-current', 'step');
    }});
  }}, {{ rootMargin: '-30% 0px -60% 0px' }});
  document.querySelectorAll('.step, .help').forEach(function (s) {{ io.observe(s); }});
}})();
</script>
"""


def render(app):
    toc, steps = [], []
    for i, s in enumerate(app["steps"], 1):
        sid = f"step-{i}"
        toc.append(f'      <li><a href="#{sid}"><span class="n">{i}</span>{html.escape(s["title"])}</a></li>')
        do = "".join(f"<li><span>{x}</span></li>" for x in s["do"])
        fix = ""
        if s["fix"]:
            fix = ('<details class="fix"><summary>If it doesn\'t work</summary><ul>'
                   + "".join(f"<li>{x}</li>" for x in s["fix"]) + "</ul></details>")
        cls = "step wide" if s.get("wide") else "step"
        fig_cls = "frame low" if s.get("crop") == "low" else "frame"
        steps.append(
            f'    <section class="{cls}" id="{sid}">\n'
            f'      <div class="step-text">\n'
            f'        <p class="step-n">Step {i} of {len(app["steps"])}</p>\n'
            f'        <h2>{html.escape(s["title"])}</h2>\n'
            f'        <p>{s["text"]}</p>\n'
            f'        <ol class="do">{do}</ol>\n'
            f'        {fix}\n'
            f'      </div>\n'
            f'      <figure class="{fig_cls}"><img src="{{{{assets}}}}howto/{s["img"]}" alt="{html.escape(s["alt"])}" loading="lazy"></figure>\n'
            f'    </section>')
    desc = f'Step-by-step guide to {app["name"]} for {app["where"]}, with pictures of every step and fixes for common problems.'
    return PAGE.format(name=app["name"], where=app["where"], slug=app["slug"], lede=app["lede"], minutes=app["minutes"],
                       plan=app["plan"], desc=desc, toc="\n".join(toc), steps="\n".join(steps))


def write():
    for app in APPS:
        out = ROOT / "src" / "guides" / f"how-to-use-{app['slug']}.html"
        out.write_text(render(app))


if __name__ == "__main__":
    write()
    print("wrote", [f"how-to-use-{a['slug']}.html" for a in APPS])
