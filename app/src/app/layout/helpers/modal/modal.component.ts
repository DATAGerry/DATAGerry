import { Component, Input } from '@angular/core';

import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';


@Component({
  // tslint:disable-next-line:component-selector
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent {

  @Input() title = 'Information';
  @Input() modalIcon = 'trash';
  @Input() modalMessage = 'Are you sure, you want to delete all selected objects?';
  @Input() subModalMessage = '';
  @Input() buttonDeny = 'Cancel';
  @Input() buttonAccept = 'Accept';

  constructor(public activeModal: NgbActiveModal) {}

}
