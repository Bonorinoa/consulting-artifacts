Surgical change only. Do not redesign the page.

On `/consulting`, the Midstream evidence row currently includes a dead label:

    { label: 'Interactive demo — in build' }

That demo is now live. Change that object to:

    { label: 'Interactive demo', href: 'https://cvprofiles-demo.streamlit.app/' }

Keep the other two Midstream links (Substack, GitHub) exactly as they are.

The existing renderer already treats `href` as an external link (`target="_blank"` rel="noreferrer"). Do not wrap the demo in an iframe, a screenshot, a new section, or extra copy. Do not add the URL anywhere else (nav, footer, Academic page) unless it already says "in build".

If you find any other occurrence of "Interactive demo — in build" or "in build" referring to this demo, update those the same way.

Leave layout, tokens, stages, copy, and the split panel untouched.

After the edit: give me a 5-line plan of what you changed, then implement. Flag if you would do it differently.
