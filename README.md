# This example demonstrates some advanced design patterns

# Optional Design Patterns
- only try these if you are not struggling with the more basic patterns you first learn in django

## multiple views & template sub folders - better organization
- Splitting views is useful when you have more than one model, e.g., `User` and `Task` and you want to have a route for all users and a route for all tasks, you can't have the two view functions with the name 'all' and two html files named 'all' unless they are split into separate view files and separate template sub-folders

## [Split models into multiple files](https://chrisbartos.com/articles/how-to-organize-your-models/)
- implemented in same way as multiple views

## `base.html` pattern & `include`
- `include` is used to include all the HTML from another file, can be used for re-usable or just separating out a distinct section of HTML to keep things from getting bloated
- [Django Girls base.html tutorial](https://tutorial.djangogirls.org/en/template_extending/)
- create a block in the head of the `base.html` that you can use to inject stylesheet `<link>` tags into from other html files
  - e.g., your extension html file has it's own personal stylesheet that you need the `base.html` to load
- create a block in between the `<title>` if you want each page to be able to set the `<title>` of the html page

## Fat models, skinny views
- move all the logic that relates to the model onto the model itself to keep that separate from the views (separation of concerns)