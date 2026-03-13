from shiny import App, render, ui

ui = ui.page_fixed(
    ui.panel_title(ui.h2("Basic Shiny App", class_="pt-5")),
    ui.output_text("test_text")
)

def server(input):
    @render.text
    def test_text():
        return "this is my first python shiny app"    

app = App(ui, server)