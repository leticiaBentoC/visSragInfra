import dash_bootstrap_components as dbc

def generate_header():
    
    search_navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("Visualização de Dados - Síndrome Respiratória Aguda", href="#"),
            ]
        ),
        className="mb-5",
    )
    
    return search_navbar