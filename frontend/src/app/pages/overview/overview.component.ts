import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DatePickerModule } from 'primeng/datepicker';
import { MockDataService, MealItem, FoodLogs } from '../../services/mock-data.service';
import { MealItemComponent } from '../../components/meal-item/meal-item.component';

@Component({
  selector: 'app-overview',
  standalone: true,
  imports: [CommonModule, FormsModule, DatePickerModule, MealItemComponent],
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.css']
})
export class OverviewComponent implements OnInit {
  date: Date | undefined = new Date();
  breakfastItems: MealItem[] = [];
  lunchItems: MealItem[] = [];
  dinnerItems: MealItem[] = [];
  isLoading = false;

  addingBreakfast = false;
  newBreakfastItem: MealItem = { name: '', quantity: 1, serving: '', calories: 0 };

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
}
