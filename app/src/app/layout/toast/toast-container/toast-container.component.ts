import {AfterViewChecked, ChangeDetectorRef, Component, HostBinding, OnInit, TemplateRef} from '@angular/core';
import { ToastService } from '../toast.service';
import {animate, state, style, transition, trigger} from '@angular/animations';


@Component({
  selector: 'cmdb-toast-container',
  templateUrl: './toast-container.component.html',
  styleUrls: ['./toast-container.component.scss'],
  animations: [
    // the fade-in/fade-out animation.
    trigger('simpleFadeAnimation', [

      // the "in" style determines the "resting" state of the element when it is visible.
      state('in', style({opacity: 1})),

      // fade in when created.
      transition(':enter', [
        style({opacity: 0}),
        animate(500 )
      ]),

      // fade out when destroyed. this could also be written as transition('void => *')
      transition(':leave',
        animate(500, style({opacity: 0})))
    ])
  ]
})


export class ToastContainerComponent implements AfterViewChecked{
  // public toastTopRight: boolean;
  // public toastTopLeft: boolean;
  // public toastBottomRight: boolean;
  // public toastBottomLeft: boolean;
  // public toastCenter: boolean;

  constructor(public toastService: ToastService, public changeDetector: ChangeDetectorRef) {
    // this.toastTopRight = true;
    // this.toastBottomLeft = false;
    // this.toastBottomRight = false;
    // this.toastTopLeft = false;
    // this.toastCenter = false;
  }

  // @HostBinding('class.ngb-toasts-bottom-left') get s() { return this.toastBottomLeft; }
  // @HostBinding('class.ngb-toasts-bottom-right') get r() { return this.toastBottomRight; }
  // @HostBinding('class.ngb-toasts-top-left') get q() { return this.toastTopLeft; }
  // @HostBinding('class.ngb-toasts-top-right') get t() { return this.toastTopRight; }
  // @HostBinding('class.ngb-toasts-center') get u() { return this.toastCenter; }

  public progress: number = 0;

  ngAfterViewChecked() {
    this.changeDetector.detectChanges();
  }
  //
  // disableAllHostBinding() {
  //   this.toastTopLeft = false;
  //   this.toastBottomLeft = false;
  //   this.toastBottomRight = false;
  //   this.toastCenter = false;
  //   this.toastTopRight = false;
  // }
  //
  // setDirection(direction: string) {
  //   switch (direction) {
  //     case 'bottom-right': {
  //       this.disableAllHostBinding();
  //       this.toastBottomRight = true;
  //       break;
  //     }
  //     case 'top-left': {
  //       this.disableAllHostBinding();
  //       this.toastTopLeft = true;
  //       break;
  //     }
  //     case 'bottom-left': {
  //       this.disableAllHostBinding();
  //       this.toastBottomLeft = true;
  //       break;
  //     }
  //     case 'center': {
  //       this.disableAllHostBinding();
  //       this.toastCenter = true;
  //       break;
  //     }
  //     default: {
  //       this.disableAllHostBinding();
  //       this.toastTopRight = true;
  //       break;
  //     }
  //   }
  // }

  disposeToast(toast) {
    this.toastService.remove(toast);
  }

  isTemplate(toast) {
    return toast.textOrTpl instanceof TemplateRef;
  }

  parse(time: number) {
    if (time) {
      return 'progressBars ' + time.toString() + ' s linear';
    }
    return 'progressBar 10s linear';
  }

  waitTillDisposal(time: number, toast) {
    // tslint:disable-next-line:only-arrow-functions
    function delay(ms: number) {
      return new Promise( resolve => {
        setTimeout(resolve, ms);
      });
    }

    (async () => {
      await delay(time);
      if (toast) {
        this.disposeToast(toast);
      }
    })();
  }

}
