import psycopg2

def calculate_stroke_play_score_from_db(host, database, user, password, table_name, player1_name, player2_name):
    """
    Calculates the winner of a stroke play golf game between two players
    based on hole-by-hole scores and handicaps from a PostgreSQL database.

    Args:
        host (str): The database server hostname.
        database (str): The name of the database.
        user (str): The database username.
        password (str): The database password.
        table_name (str): The name of the table containing the golf match data.
        player1_name (str): The name of player 1.
        player2_name (str): The name of player 2.

    Returns:
        tuple: (winner_name, result_string)
            - winner_name (str): The name of the winning player, or "Tie" if the match is tied.
            - result_string (str): A string describing the match result.
            Returns None, None if there is an error.
    """
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()

        # Construct the SQL query to fetch player data and scores
        query = f"""
            SELECT
                p1.player_name AS player1_name,
                p1.handicap AS player1_handicap,
                p2.player_name AS player2_name,
                p2.handicap AS player2_handicap,
                r.hole1_score_p1, r.hole1_score_p2,
                r.hole2_score_p1, r.hole2_score_p2,
                r.hole3_score_p1, r.hole3_score_p2,
                r.hole4_score_p1, r.hole4_score_p2,
                r.hole5_score_p1, r.hole5_score_p2,
                r.hole6_score_p1, r.hole6_score_p2,
                r.hole7_score_p1, r.hole7_score_p2,
                r.hole8_score_p1, r.hole8_score_p2,
                r.hole9_score_p1, r.hole9_score_p2,
                r.hole10_score_p1, r.hole10_score_p2,
                r.hole11_score_p1, r.hole11_score_p2,
                r.hole12_score_p1, r.hole12_score_p2,
                r.hole13_score_p1, r.hole13_score_p2,
                r.hole14_score_p1, r.hole14_score_p2,
                r.hole15_score_p1, r.hole15_score_p2,
                r.hole16_score_p1, r.hole16_score_p2,
                r.hole17_score_p1, r.hole17_score_p2,
                r.hole18_score_p1, r.hole18_score_p2
            FROM
                {table_name} r
            JOIN
                players p1 ON r.player1_id = p1.player_id
            JOIN
                players p2 ON r.player2_id = p2.player_id
            WHERE p1.player_name = %s AND p2.player_name = %s
            """
        cursor.execute(query, (player1_name, player2_name))
        result = cursor.fetchone()

        if result is None:
            print(f"Error: No match found for players {player1_name} and {player2_name}")
            return None, None

        # Extract data from the result tuple
        player1_name_db, player1_handicap = result[0], result[1]
        player2_name_db, player2_handicap = result[2], result[3]
        player1_scores = [result[i] for i in range(4, 39, 2)]  # Extract player 1's scores
        player2_scores = [result[i] for i in range(5, 40, 2)]  # Extract player 2's scores

        # Calculate adjusted scores based on handicaps
        player1_adjusted_score = sum(player1_scores) - player1_handicap
        player2_adjusted_score = sum(player2_scores) - player2_handicap

        # Determine the winner and format the result string
        if player1_adjusted_score < player2_adjusted_score:
            winner_name = player1_name_db
            result_string = f"{player1_name_db} wins with a score of {player1_adjusted_score}"
        elif player2_adjusted_score < player1_adjusted_score:
            winner_name = player2_name_db
            result_string = f"{player2_name_db} wins with a score of {player2_adjusted_score}"
        else:
            winner_name = "Tie"
            result_string = f"Match tied with both players scoring {player1_adjusted_score}"

        return winner_name, result_string

    except psycopg2.Error as e:
        print(f"Error connecting to or querying the database: {e}")
        return None, None
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    # Database connection parameters
    host = "127.0.0.1"       # Replace with your database host
    database = "golf_db" # Replace with your database name
    user = "postgres"     # Replace with your database username
    password = "password" # Replace with your database password
    table_name = "Scores"  # Replace with your table name
    player1_name = "Tiger Woods"  # Replace with the actual player names you want to query
    player2_name = "Phil Mickelson"

    winner, result = calculate_stroke_play_score_from_db(host, database, user, password, table_name, player1_name, player2_name)

    if winner:
        print("Winner:", winner)
        print("Result:", result)
    else:
        print("Could not calculate stroke play score.")

