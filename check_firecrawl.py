import firecrawl
fc = firecrawl.FirecrawlApp(api_key='test')
print([m for m in dir(fc) if not m.startswith('_')])
