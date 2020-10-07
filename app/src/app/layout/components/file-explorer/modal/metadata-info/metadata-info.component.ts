import {Component, Input, OnInit} from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FileElement } from '../../model/file-element';
import { BehaviorSubject } from 'rxjs';
import { ObjectService } from '../../../../../framework/services/object.service';
import { CmdbType } from '../../../../../framework/models/cmdb-type';
import { TypeService } from '../../../../../framework/services/type.service';
import { RenderResult } from '../../../../../framework/models/cmdb-render';
import { UserService } from '../../../../../management/services/user.service';

@Component({
  selector: 'cmdb-metadata-info',
  templateUrl: './metadata-info.component.html',
  styleUrls: ['./metadata-info.component.scss']
})
export class MetadataInfoComponent implements OnInit {

  /**
   * Data sharing between components
   */
  @Input() folderTree: FileElement[] = [];
  @Input() fileElement: FileElement;

  public selectedFileFolder: BehaviorSubject<any> = new BehaviorSubject<any>(null);
  public cmdbObject: RenderResult = null;
  public cmdbType: CmdbType = null;
  public navigationLink: string;
  public username: string;
  public refId: number;
  public refType: string;

  constructor(public activeModal: NgbActiveModal, private objectService: ObjectService,
              private typeService: TypeService, private userService: UserService) {}

  ngOnInit(): void {
    const tempFile: any = Object.assign({}, this.fileElement);
    tempFile.public_id = this.fileElement.metadata.parent;
    this.selectedFileFolder.next(tempFile);

    this.userService.getUser(this.fileElement.metadata.author_id).subscribe(user => {
      this.username = `${user.user_name}`;
    });

    this.refId = this.fileElement.metadata.reference;
    this.refType = this.fileElement.metadata.reference_type;
    this.refType = this.refType ? this.refType : 'None';
    switch (this.refType) {
      case 'object': {
        this.objectService.getObject<RenderResult>(this.refId).subscribe((obj: RenderResult) => {
          this.cmdbObject = obj;
          this.navigationLink = `/framework/object/type/view/${this.refId}`;
        });
        break;
      }
      case 'type': {
        this.typeService.getType(this.refId).subscribe((obj: CmdbType) => {
          this.cmdbType = obj;
          this.navigationLink = `/framework/object/type/view/${this.refId}`;
        });
        break;
      }
    }
  }

}
