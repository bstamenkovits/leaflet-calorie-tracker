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
  date: Date | undefined = new Date();

  increaseDate() {
    if (this.date) {
      const nextDate = new Date(this.date);
      nextDate.setDate(nextDate.getDate() + 1);
      this.date = nextDate;
      console.log(this.date);
      // update page content based on the new date
    }
  }

  decreaseDate() {
    if (this.date) {
      const nextDate = new Date(this.date);
      nextDate.setDate(nextDate.getDate() - 1);
      this.date = nextDate;
      console.log(this.date);
      // update page content based on the new date
    }
  }
}
