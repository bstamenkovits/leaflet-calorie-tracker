import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { delay } from 'rxjs/operators';

export interface FoodItem {
  name: string;
  quantity: number;
  serving: string;
  calories: number;
}

export interface FoodLogs {
  breakfast: FoodItem[];
  lunch: FoodItem[];
  dinner: FoodItem[];
}

@Injectable({
  providedIn: 'root'
})
export class MockDataService {
  private readonly breakfastOptions: FoodItem[] = [
    { name: 'Scrambled Eggs', quantity: 2, serving: 'egg(s)', calories: 180 },
    { name: 'Oatmeal', quantity: 1, serving: 'cup(s)', calories: 150 },
    { name: 'Berries', quantity: 0.5, serving: 'cup(s)', calories: 40 },
    { name: 'Avocado Toast', quantity: 1, serving: 'slice(s)', calories: 320 },
    { name: 'Greek Yogurt', quantity: 1, serving: 'cup(s)', calories: 150 },
    { name: 'Granola', quantity: 0.5, serving: 'cup(s)', calories: 130 },
    { name: 'Banana', quantity: 1, serving: 'piece(s)', calories: 105 },
    { name: 'Pancakes', quantity: 3, serving: 'piece(s)', calories: 270 },
    { name: 'Maple Syrup', quantity: 2, serving: 'tbsp', calories: 100 },
    { name: 'Protein Shake', quantity: 1, serving: 'serving(s)', calories: 220 },
    { name: 'Bagel', quantity: 1, serving: 'piece(s)', calories: 245 },
    { name: 'Cream Cheese', quantity: 2, serving: 'tbsp', calories: 100 },
    { name: 'Orange Juice', quantity: 1, serving: 'cup(s)', calories: 110 },
    { name: 'Coffee', quantity: 1, serving: 'cup(s)', calories: 5 }
  ];

  private readonly lunchOptions: FoodItem[] = [
    { name: 'Grilled Chicken', quantity: 4, serving: 'oz', calories: 180 },
    { name: 'Caesar Salad', quantity: 1, serving: 'bowl(s)', calories: 250 },
    { name: 'Turkey Sandwich', quantity: 1, serving: 'sandwich(es)', calories: 320 },
    { name: 'Tomato Soup', quantity: 1, serving: 'cup(s)', calories: 120 },
    { name: 'Quinoa Bowl', quantity: 1, serving: 'bowl(s)', calories: 280 },
    { name: 'Pasta Salad', quantity: 1, serving: 'cup(s)', calories: 200 },
    { name: 'Chicken Wrap', quantity: 1, serving: 'wrap(s)', calories: 350 },
    { name: 'Sushi Roll', quantity: 8, serving: 'piece(s)', calories: 300 },
    { name: 'Veggie Burger', quantity: 1, serving: 'burger(s)', calories: 250 },
    { name: 'French Fries', quantity: 1, serving: 'serving(s)', calories: 220 },
    { name: 'Side Salad', quantity: 1, serving: 'bowl(s)', calories: 80 },
    { name: 'Apple', quantity: 1, serving: 'piece(s)', calories: 95 }
  ];

  private readonly dinnerOptions: FoodItem[] = [
    { name: 'Grilled Salmon', quantity: 6, serving: 'oz', calories: 280 },
    { name: 'Roasted Vegetables', quantity: 1, serving: 'cup(s)', calories: 120 },
    { name: 'Brown Rice', quantity: 1, serving: 'cup(s)', calories: 215 },
    { name: 'Steak', quantity: 8, serving: 'oz', calories: 450 },
    { name: 'Baked Potato', quantity: 1, serving: 'piece(s)', calories: 160 },
    { name: 'Spaghetti', quantity: 1, serving: 'cup(s)', calories: 220 },
    { name: 'Marinara Sauce', quantity: 0.5, serving: 'cup(s)', calories: 80 },
    { name: 'Chicken Breast', quantity: 6, serving: 'oz', calories: 180 },
    { name: 'Sweet Potato', quantity: 1, serving: 'piece(s)', calories: 180 },
    { name: 'Broccoli', quantity: 1, serving: 'cup(s)', calories: 55 },
    { name: 'Pork Chop', quantity: 5, serving: 'oz', calories: 220 },
    { name: 'Green Beans', quantity: 1, serving: 'cup(s)', calories: 40 },
    { name: 'Garlic Bread', quantity: 2, serving: 'slice(s)', calories: 180 }
  ];

  constructor() {}

  /**
   * Get food logs for a specific date
   * Returns breakfast, lunch, and dinner items
   * Simulates API delay and returns random items for each meal
   */
  getFoodLogs(date: Date): Observable<FoodLogs> {
    const foodLogs: FoodLogs = {
      breakfast: this.generateMealItems(this.breakfastOptions, 2, 4),
      lunch: this.generateMealItems(this.lunchOptions, 2, 5),
      dinner: this.generateMealItems(this.dinnerOptions, 3, 5)
    };

    // Simulate API delay (300ms)
    return of(foodLogs).pipe(delay(300));
  }

  /**
   * Helper method to generate random meal items
   */
  private generateMealItems(options: FoodItem[], minItems: number, maxItems: number): FoodItem[] {
    const itemCount = Math.floor(Math.random() * (maxItems - minItems + 1)) + minItems;
    const items: FoodItem[] = [];
    const selectedIndices = new Set<number>();

    while (items.length < itemCount && selectedIndices.size < options.length) {
      const randomIndex = Math.floor(Math.random() * options.length);

      if (!selectedIndices.has(randomIndex)) {
        selectedIndices.add(randomIndex);
        items.push({ ...options[randomIndex] });
      }
    }

    return items;
  }
}
