import { Component, Input } from '@angular/core';
import { MealItem } from '../../services/mock-data.service';

@Component({
  selector: 'meal-item',
  standalone: true,
  imports: [],
  templateUrl: './meal-item.component.html',
  styleUrls: ['./meal-item.component.css']
})
export class MealItemComponent {
  @Input({ required: true }) item!: MealItem;
  isExpanded = false;
}
