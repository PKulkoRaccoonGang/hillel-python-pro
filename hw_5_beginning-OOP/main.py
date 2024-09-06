from flask import Flask, jsonify
from webargs import fields
from webargs.flaskparser import use_kwargs
from database_handler import execute_query


app = Flask(__name__)


@app.route('/popular_genres_by_city')
@use_kwargs({'genre': fields.Str(load_default=None)}, location='query')
def get_popular_genre_cities(genre):
    """
    Endpoint to find cities where a specific music genre is most popular.

    This function retrieves cities where a specified music genre has the highest number
    of purchases based on sales data. If no genre is provided, it returns an error message.

    Args:
        genre (str): The name of the music genre passed as a query parameter. If not provided,
                     a 400 error response is returned.

    Returns:
        JSON response containing a list of cities where the genre is most popular,
        including the city name, genre, and the number of purchases.

    Example response:
    [
        {
            "city": "Orlando",
            "genre": "Rock And Roll",
            "purchase_count": 15
        },
        {
            "city": "New York",
            "genre": "Rock And Roll",
            "purchase_count": 12
        }
    ]
    """
    if genre:
        query = """
        SELECT
            City,
            Name AS Genre,
            GenreCounts AS PurchaseCount
        FROM
            (SELECT
                customers.City,
                genres.Name,
                COUNT(*) AS GenreCounts,
                DENSE_RANK() OVER (PARTITION BY genres.Name ORDER BY COUNT(*) DESC) AS DRank
            FROM
                customers
                JOIN invoices ON customers.CustomerId = invoices.CustomerId
                JOIN invoice_items ON invoices.InvoiceId = invoice_items.InvoiceId
                JOIN tracks ON invoice_items.TrackId = tracks.TrackId
                JOIN genres ON tracks.GenreId = genres.GenreId
            WHERE
                genres.Name = ?
            GROUP BY
                customers.City,
                genres.Name) AS ranked_cities
        WHERE
            DRank = 1
        ORDER BY
            GenreCounts DESC
        ;
        """
        query_result = execute_query(query=query, args=(genre,))
    else:
        return jsonify({"error": "Please provide a genre name."}), 400

    response_data = []

    for row in query_result:
        city = row[0]
        genre_name = row[1] if len(row) > 1 else None
        purchase_count = row[2] if len(row) > 2 else None

        response_data.append({
            'city': city,
            'genre': genre_name,
            'purchase_count': purchase_count
        })

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(port=5006, debug=True)
