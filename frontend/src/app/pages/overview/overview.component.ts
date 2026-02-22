import { Component } from '@angular/core';
// import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DatePickerModule } from 'primeng/datepicker';

@Component({
  selector: 'app-overview',
  standalone: true,
  imports: [FormsModule, DatePickerModule],
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.css']
})
export class OverviewComponent {
  currentDate = new Date();
  selectedDate = new Date();
  date: Date | undefined = new Date();
  selectedDateString = this.formatDateForInput(new Date());

  formatDateForInput(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  onDateChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.value) {
      this.selectedDate = new Date(input.value + 'T00:00:00');
      this.selectedDateString = input.value;
    }
  }
}
