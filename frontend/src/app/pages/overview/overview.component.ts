import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DatePickerModule } from 'primeng/datepicker';
import { MockDataService, FoodItem, FoodLogs } from '../../services/mock-data.service';

@Component({
  selector: 'app-overview',
  standalone: true,
  imports: [CommonModule, FormsModule, DatePickerModule],
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.css']
})
export class OverviewComponent implements OnInit {
  date: Date | undefined = new Date();
  breakfastItems: FoodItem[] = [];
  lunchItems: FoodItem[] = [];
  dinnerItems: FoodItem[] = [];
  isLoading = false;

  constructor(
    private mockDataService: MockDataService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    console.log(this.date);
    this.loadFoodLogs();
  }

  loadFoodLogs() {
    if (!this.date) return;

    console.log('Loading food logs for date:', this.date);

    this.isLoading = true;
    this.mockDataService.getFoodLogs(this.date).subscribe({
      next: (foodLogs: FoodLogs) => {
        console.log('Food logs received:', foodLogs);
        this.breakfastItems = foodLogs.breakfast;
        this.lunchItems = foodLogs.lunch;
        this.dinnerItems = foodLogs.dinner;
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error loading food logs:', error);
        this.isLoading = false;
      }
    });
  }

  increaseDate() {
    if (this.date) {
      const nextDate = new Date(this.date);
      nextDate.setDate(nextDate.getDate() + 1);
      this.date = nextDate;
      console.log(this.date);
      this.loadFoodLogs();
    }
  }

  decreaseDate() {
    if (this.date) {
      const nextDate = new Date(this.date);
      nextDate.setDate(nextDate.getDate() - 1);
      this.date = nextDate;
      console.log(this.date);
      this.loadFoodLogs();
    }
  }

  deleteItem(mealType: 'breakfast' | 'lunch' | 'dinner', item: FoodItem) {
    switch(mealType) {
      case 'breakfast':
        this.breakfastItems = this.breakfastItems.filter(i => i !== item);
        break;
      case 'lunch':
        this.lunchItems = this.lunchItems.filter(i => i !== item);
        break;
      case 'dinner':
        this.dinnerItems = this.dinnerItems.filter(i => i !== item);
        break;
    }
    this.cdr.detectChanges();
  }
}
