import {Component} from '@angular/core';
import {ToastService} from '../toast.service';
import {animate, state, style, transition, trigger} from '@angular/animations';


@Component({
  selector: 'cmdb-toast-container',
  templateUrl: './toast-container.component.html',
  styleUrls: ['./toast-container.component.scss'],
  animations: [
    // the fade-in/fade-out animation.
    trigger('simpleFadeAnimation', [

      state('in', style({opacity: 1})),

      transition(':enter', [
        style({opacity: 0}),
        animate(500 )
      ]),

      transition(':leave',
        animate(500, style({opacity: 0})))
    ])
  ]
})


export class ToastContainerComponent {

  constructor(public toastService: ToastService) {
  }


}
