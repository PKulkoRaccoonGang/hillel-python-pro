from flask import Flask, jsonify

from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from database_handler import execute_query


app = Flask(__name__)


@app.route('/order-price/sales-country')
@use_kwargs({'country': fields.Str(load_default=None)}, location='query')
def get_country_sales(country: str = None):
    """Retrieves the total sales amount either for a specific country or globally."""
    try:
        if country:
            select_total_by_country_query = "SELECT SUM(Total) FROM invoices WHERE BillingCountry = ?"
            total_by_country_data = execute_query(select_total_by_country_query, (country,))

            result = {
                'country': f'Sum of sales for {country}',
                'total': str(*total_by_country_data[0])
            }

        else:
            country_and_total_invoices_query = "SELECT SUM(Total) FROM invoices"
            country_and_total_invoices_data = execute_query(query=country_and_total_invoices_query)

            result = {
                'message': 'Sum of sales',
                'total': str(*country_and_total_invoices_data[0])
            }

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/order-price/sales-total')
def get_total_sales():
    """Retrieves the total sales amount from the invoice_items table."""
    try:
        query = "SELECT SUM(UnitPrice * Quantity) as TotalSales FROM invoice_items"
        total_sales = execute_query(query=query)

        if total_sales:
            total_sales = total_sales[0][0]
        else:
            total_sales = 0

        return jsonify({'sales': total_sales})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/order-price/sales-info')
def get_sales_info():
    """Retrieves sales information by joining invoices and invoice_items tables."""
    try:
        query = """
            SELECT 
                invoices.InvoiceId, 
                invoices.BillingCountry, 
                invoice_items.TrackId, 
                invoice_items.UnitPrice, 
                invoice_items.Quantity 
            FROM invoices 
            INNER JOIN invoice_items ON invoices.InvoiceId = invoice_items.InvoiceId;
        """
        results = execute_query(query=query)

        sales_info = [
            {
                "invoice_id": row[0],
                "billing_country": row[1],
                "track_id": row[2],
                "unit_price": row[3],
                "quantity": row[4]
            }
            for row in results
        ]

        return jsonify({"sales_info": sales_info})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/track-info')
@use_kwargs({'track_id': fields.Int(load_default=12, validate=validate.Range(min=1))}, location='query')
def get_info_about_track(track_id):
    """
    Retrieve detailed information about a track based on its ID.
    """
    try:
        query = """
            SELECT 
                tracks.TrackId, 
                tracks.Name AS TrackName, 
                albums.Title AS AlbumTitle, 
                artists.Name AS ArtistName, 
                genres.Name AS GenreName, 
                tracks.Composer, 
                tracks.Milliseconds, 
                tracks.Bytes, 
                tracks.UnitPrice 
            FROM tracks
            JOIN albums ON tracks.AlbumId = albums.AlbumId
            JOIN artists ON albums.ArtistId = artists.ArtistId
            JOIN genres ON tracks.GenreId = genres.GenreId
            WHERE tracks.TrackId = ?;
        """

        data = execute_query(query, (track_id,))

        if not data:
            return jsonify({"error": "Track not found"}), 404

        track_info = {
            "track_id": data[0][0],
            "track_name": data[0][1],
            "album_title": data[0][2],
            "artist_name": data[0][3],
            "genre_name": data[0][4],
            "composer": data[0][5],
            "milliseconds": data[0][6],
            "bytes": data[0][7],
            "unit_price": data[0][8]
        }

        return jsonify(track_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tracks-duration')
def get_tracks_duration():
    """Retrieves the total duration of all tracks in hours."""
    try:
        query = "SELECT SUM(Milliseconds) / 3600000 AS TotalHours FROM tracks;"
        result = execute_query(query=query)

        total_hours = result[0][0] if result and result[0][0] is not None else 0

        return jsonify({'tracks_duration_hours': total_hours}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5003, debug=True)
