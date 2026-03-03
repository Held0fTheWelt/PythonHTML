"""
Practice: API with Python
Sucht über The Meal DB API nach Mahlzeiten und zeigt die gefundenen Rezepte an.
Verwendet response.json() für die JSON-Antwort der API.
"""
import requests

API_URL = "https://www.themealdb.com/api/json/v1/1/search.php"


def get_ingredients(meal):
    """Sammelt alle nicht leeren Zutaten mit Menge aus dem Meal-Dict."""
    ingredients = []
    for i in range(1, 21):
        ing = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}") or ""
        if ing and ing.strip():
            part = f"{measure.strip()} {ing}".strip() if measure else ing
            ingredients.append(part)
    return ingredients


def display_meal(meal, index=None):
    """Gibt ein einzelnes Gericht formatiert aus."""
    prefix = f"\n--- Meal {index} ---\n" if index is not None else "\n"
    lines = [
        f"{prefix}*** {meal['strMeal']} ***",
        f"Category: {meal.get('strCategory', 'N/A')}",
        f"Area: {meal.get('strArea', 'N/A')}",
    ]
    if meal.get("strTags"):
        lines.append(f"Tags: {meal['strTags']}")
    lines.append("Instructions:")
    lines.append(meal.get("strInstructions", "N/A"))
    ingredients = get_ingredients(meal)
    if ingredients:
        lines.append("\nIngredients:")
        for ing in ingredients:
            lines.append(f"  - {ing}")
    print("\n".join(lines))


def main():
    meal_name = input("Enter meal name: ").strip()
    if not meal_name:
        print("No meal name entered.")
        return

    response = requests.get(API_URL, params={"s": meal_name})
    data = response.json()

    meals = data.get("meals")
    if not meals:
        print(f"No meals found for '{meal_name}'.")
        return

    n = len(meals)
    print(f"\nWe found {n} meal{'s' if n != 1 else ''}:")
    for i, meal in enumerate(meals, start=1):
        display_meal(meal, index=i if len(meals) > 1 else None)


if __name__ == "__main__":
    main()
