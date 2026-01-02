from futbolfantasy_analytics import get_futbolfantasy_data, find_manual_similar_string
from laligafantasy import get_laligafantasy_data, get_player_last_5_weeks

def find_player_futbolfantasy(name, force_scrape=False):
    """
    Busca un jugador por nombre en todo el dataset de FutbolFantasy.
    Devuelve un diccionario con club, price, position, form, start_probability y price_trend.
    """
    prices_data, positions_data, forms_data, start_probabilities_data, price_trends_data = get_futbolfantasy_data(force_scrape=force_scrape)
    
    name_lower = name.lower()
    
    for club, players in prices_data.items():
        for player_name, price in players.items():
            if player_name.lower() == name_lower:
                return {
                    "club": club,
                    "price": price,
                    "position": positions_data.get(club, {}).get(player_name),
                    "form": forms_data.get(club, {}).get(player_name),
                    "start_probability": start_probabilities_data.get(club, {}).get(player_name),
                    "price_trend": price_trends_data.get(club, {}).get(player_name)
                }
    
    return None


def find_player_laligafantasy_points(name, force_scrape=False):
    """
    Busca el jugador en LaLigaFantasy y calcula:
    - total de puntos
    - media de puntos últimos 5 partidos (si no jugó, cuenta 0)
    """
    players = get_laligafantasy_data(force_scrape=force_scrape)
    name_lower = name.lower()
    
    for player in players:
        if player.name.lower() == name_lower:
            # Suponiendo que player.points es total de puntos
            total_points = getattr(player, "points", 0)
            
            # Para los últimos 5 partidos
            last_matches = getattr(player, "fitness", [])[-5:]  # puede ser una lista de puntos por partido
            # Si la lista es más corta que 5, completamos con 0
            last_matches = [p if p is not None else 0 for p in last_matches]
            while len(last_matches) < 5:
                last_matches.insert(0, 0)
            
            avg_last_5 = sum(last_matches)/5
            return {
                "total_points": total_points,
                "avg_last_5": avg_last_5
            }
    
    return None


# Ejemplo de uso combinando todo
player_name = "Raphinha"

ff_data = find_player_futbolfantasy(player_name)

if ff_data:
    print("FutbolFantasy info:")
    print(ff_data)

stats = get_player_last_5_weeks("Raphinha")
print(stats)
