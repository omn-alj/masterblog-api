from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required.'}), 400

    # Generate a new unique ID for the post
    new_id = generate_unique_id()

    # Create the new post dictionary
    new_post = {
        'id': new_id,
        'title': data['title'],
        'content': data['content']
    }

    # Add the new post to the list of posts
    POSTS.append(new_post)

    # Return the new post with the generated ID
    return jsonify(new_post), 201

def generate_unique_id():
    if len(POSTS) > 0:
        last_id = POSTS[-1]['id']
        new_id = last_id + 1
    else:
        new_id = 1
    return new_id

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = find_post_by_id(id)

    if post is None:
        return jsonify({'error': 'Post not found.'}), 404

    POSTS.remove(post)

    return jsonify({'message': f'Post with id {id} has been deleted successfully.'}), 200

def find_post_by_id(id):
    for post in POSTS:
        if post['id'] == id:
            return post
    return None

@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = find_post_by_id(id)

    if post is None:
        return jsonify({'error': 'Post not found.'}), 404

    data = request.get_json()
    title = data.get('title', post['title'])
    content = data.get('content', post['content'])

    post['title'] = title
    post['content'] = content

    return jsonify({'id': post['id'], 'title': title, 'content': content}), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title', '')
    content = request.args.get('content', '')

    search_results = []
    for post in POSTS:
        if title.lower() in post['title'].lower() or content.lower() in post['content'].lower():
            search_results.append(post)

    return jsonify(search_results)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
