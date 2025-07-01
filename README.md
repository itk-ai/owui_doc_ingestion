# Project for testing OpenWebUI document preprocessering functionality.

## Cases

- [Vielses case](vielses_assist_case.md)

  [Findings from the "Vielse"s case](documentation/findings_vielse.md) 


## Alternatives

OWUI seems to have backend functionality and an endpoint to [process webpages](
https://github.com/open-webui/open-webui/blob/b5f4c85bb196c16a775802907aedd87366f58b0f/backend/open_webui/routers/retrieval.py#L1554
), but it does not seem to be tied to an UI functionality.

*Tika* can be intructed to output xHTML, which could then be  converted to 
markdown. This would provide a fairer comparison on the pipelines ability to
deduce the structure of the document.

*Docling* can directly output chunks, which are in the end what we want. It might
be desirable to use this *docling* functionality in favor of its markdown output,
as the [chunking functionality](https://docling-project.github.io/docling/concepts/chunking/) 
under the hood uses *Doclings* internal [DoclingDocument](https://docling-project.github.io/docling/concepts/docling_document/) 
format with much more info on the document structure. 

## TODO:

- Test *Tika* pipeline with xHTML and conversion to markdown
- Investigate the [process webpages](
https://github.com/open-webui/open-webui/blob/b5f4c85bb196c16a775802907aedd87366f58b0f/backend/open_webui/routers/retrieval.py#L1554
) functionality

## Links:

- [AI Platformen](https://stgai.itkdev.dk/)
- [Docling](https://docling.itkdev.dk) 
  - [dashbord](https://docling.itkdev.dk/ui)
- [Tika](https://tika.itkdev.dk/)
