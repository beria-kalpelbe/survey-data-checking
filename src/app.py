import os
import base64
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from functions import extract_metadata_set_of_images, find_all_similar_images
import tempfile
import dash_table

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define the app layout
app.layout = html.Div([
    html.H1("Similar Image Finder"),
    dcc.Upload(
        id='upload-images',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Images')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Div(id='output-image-grid')
])

@app.callback(
    Output('output-image-grid', 'children'),
    [Input('upload-images', 'contents'),
     Input('upload-images', 'filename')]
)
def display_similar_images(contents, filenames):
    # Check for no data case
    if contents is None or filenames is None:
        return []

    try:
        # Create a temporary directory to store the uploaded images
        images_paths = []
        with tempfile.TemporaryDirectory() as temp_dir:
            for content, filename in zip(contents, filenames):
                try:
                    # Ensure the content is properly base64 decoded
                    content_type, content_string = content.split(',')
                    decoded = base64.b64decode(content_string)
                    
                    # Save the file to a temporary directory
                    file_path = os.path.join(temp_dir, filename)
                    with open(file_path, 'wb') as f:
                        f.write(decoded)
                    images_paths.append(file_path)
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
                    continue

            # Check if there are images to process
            if not images_paths:
                print("No valid images to process.")
                return []

            # Find similar images (assuming function returns a dictionary)
            similar_images = find_all_similar_images(images_paths)
            
            if not similar_images:
                print("No similar images found.")
                return [html.P("No similar images found.")]

            # Construct the grid of similar images and metadata
            image_grid = []
            for group, image_list in similar_images.items():
                image_grid.append(
                    html.Div([
                        html.H3(f"Group {group}"),
                        html.Div([
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    base64.b64encode(open(image_path, 'rb').read()).decode()
                                ),
                                style={'height': '200px', 'width': 'auto', 'margin': '10px'}
                            ) for image_path in image_list
                        ], style={'display': 'flex', 'flex-wrap': 'wrap'}),
                        # html.Div([
                        #     get_image_metadata(image_path) for image_path in image_list
                        # ])
                    ], style={'margin': '20px'})
                )
            
            return image_grid

    except Exception as e:
        print(f"Error in callback: {e}")
        return [html.P("An error occurred while processing the images.")]

# Helper function to get image metadata
def get_image_metadata(image_path):
    try:
        metadata = extract_metadata_set_of_images([image_path])
        
        return dash_table.DataTable(
            data=metadata.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in metadata.columns],
            page_size=10
        )
    except Exception as e:
        print(f"Error retrieving metadata for {image_path}: {e}")
        return html.P(f"Could not retrieve metadata for {image_path}")

if __name__ == '__main__':
    app.run_server(debug=True)
