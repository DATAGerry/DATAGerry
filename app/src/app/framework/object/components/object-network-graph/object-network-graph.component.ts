/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
* Author: Kay-Uwe (Kiwi) Lorenz <tabkiwi@gmail.com>
*/

import { Component, Input, OnInit } from '@angular/core'
import { ObjectService } from 'src/app/framework/services/object.service'
import { RenderResult } from '../../../models/cmdb-render'

import { Network, DataSet } from 'vis-network/standalone'
// import { stringify } from 'querystring'

/**
 * This class represents fontawesome data to be used for caching for visjs 
 * network nodes.
 */
class FontAwesomeData {
  public fontFamily : string = "Font Awesome 5 Free"
  public content : string = ""

  // constructor (fontFamily: string, content: string) {
  //   this.fontFamily = fontFamily
  //   this.content = content
  // }
}

/** */
@Component({
  selector: 'cmdb-object-network-graph',
  templateUrl: './object-network-graph.component.html',
  styleUrls: ['./object-network-graph.component.scss']
})
export class ObjectNetworkGraphComponent {k

  private id: number
  private depth: number = 2
  private _renderResult: any
  private rendered: boolean = false

  static faMap: Record<string, FontAwesomeData> = undefined

  public referenceList: RenderResult[] = []

  public records: Record<number, RenderResult[]> = {}

  public recordsLoading: number[] = []

  @Input() renderResult: RenderResult;

  @Input()
  set publicID(publicID: number) {
    console.log('set publicID', publicID)
    this.id = publicID

    if (this.id !== undefined && this.id !== null) {
      this.loadNetworkGraphData(publicID)
    }
  }

  get publicID(): number {
    return this.id
  }

  public constructor(private objectService: ObjectService) {
    console.log('construct network-graph')
  }

  private loadNetworkGraphData(publicID: number, level: number = 1) {
    console.log("load refs for", publicID)
    
    this.renderNetworkGraph()

    console.log("renderResult", this.renderResult)

    // load the references
    this.loadObjectReferences(publicID, level)
  }

  private loadObjectReferences(publicID: number, level: number = 1) {
    console.log("load refs for", publicID)
    
    this.recordsLoading.push(1)

    this.objectService.getObjectReferences(publicID).subscribe((references: RenderResult[])  => {
      console.log("references", references)
      this.records[publicID] = references

      console.log("getObjectReferences records loading: ", this.recordsLoading.length)
      if (level < this.depth) {
        references.forEach((r) => {
          this.loadObjectReferences(r.object_information.object_id, level+1)
        })
      }
    },
    (error) => {
      console.error(error)
    },
    () => {
      this.recordsLoading.pop()
      if (this.recordsLoading.length == 0) {
        this.renderNetworkGraph()
      }
    })

  }

  private createIconMap() {
    ObjectNetworkGraphComponent.faMap = {}

    // fill map
    Array.from(document.styleSheets).forEach((S) => {

      var cssRules = null;

      try {
        cssRules = (S as CSSStyleSheet).cssRules
      }
      catch (e) {
        console.error("skip", e)
        return
      }
      // Font Awesome 5 Free
      Array.from(cssRules).forEach((r) => {
        const csr : CSSStyleRule = r as CSSStyleRule
        //console.log("csr", csr)

        if (csr.selectorText === undefined) return

        const m = csr.selectorText.match(/^(\.fa[^,\s]*?)(::?before)?$/)
        if (m == null) return

        if (!(m[1] in ObjectNetworkGraphComponent.faMap)) {
          ObjectNetworkGraphComponent.faMap[m[1]] = new FontAwesomeData()
        }

        const fad = ObjectNetworkGraphComponent.faMap[m[1]];

        if (csr.style.fontFamily !== "") {
          fad.fontFamily = csr.style.fontFamily.replace(/^"/, '').replace(/"$/, '')
        }

        if (csr.style.content !== "") {
          fad.content = csr.style.content.replace(/^"/, '').replace(/"$/, '')
        }
      })
    })

    console.log("faMap", ObjectNetworkGraphComponent.faMap)
  }

  private getIconCI(ci: RenderResult) {
    return this.getIcon(ci.type_information.icon)
  }

  private getIcon(iconInfo: string) {
    var iconName1 = ""
    var iconName2 = ""

    // get fontawsome icon name
    iconInfo.split(/\s+/).forEach((s) => {
      if (s.match(/^fa-/)) {
        iconName2 = '.'+s
      }
      iconName1 += '.'+s
    })

    // if map is empty
    if (ObjectNetworkGraphComponent.faMap === undefined) {
      this.createIconMap()
    }

    var icon: FontAwesomeData = undefined

    console.log("iconName1", iconName1, "iconName2", iconName2)

    if (iconName1 in ObjectNetworkGraphComponent.faMap) {
      icon = ObjectNetworkGraphComponent.faMap[iconName1]
    } else if (iconName2 in ObjectNetworkGraphComponent.faMap) {
      icon = ObjectNetworkGraphComponent.faMap[iconName2]
    } else {
      icon = new FontAwesomeData()
      icon.fontFamily = "sans"
      icon.content = "?"
    }

    return {
      code: icon.content,
      face: '"'+icon.fontFamily+'"',
      size: 40,
      weight: "bold"
    }


    //return faMap[iconNmae]
  }

  private renderNetworkGraph(): void {
    // if (this.rendered) return
    // this.rendered = true

    var target = document.querySelector('.object-network-graph')

    console.log('render network graph')

    // console.log("reference list", this.referenceList)

    var nodes = []
    var edges = []

    const this_ci = this.renderResult

    console.log('CI: ', this_ci)

    if (this_ci === undefined) return

    const current_node = {
      id: this_ci.object_information.object_id,
      label: this_ci.summary_line,
      shape: "icon", 
      icon: this.getIconCI(this_ci),
      //opacity: 0.7,
//      x: 0,
 //     y: 0,
      size: 40,
    }

    nodes.push(current_node)

    var edgeLength : number = 100

    console.log("current_node", current_node)

    const createNodes = (ci_obj: RenderResult) => {
      const id = ci_obj.object_information.object_id

      // add all refs this object is pointing to
      ci_obj.fields.forEach((field) => {
        if (field.type !== 'ref') return

        nodes.push({
          id: field.value,
          label: field.type_label + " #" + field.value,
          shape: "icon",
          icon: this.getIcon(field.reference.icon),
          size: 40,
        })

        edges.push({ from: id, to: field.value, length: edgeLength, arrows: "to" });
      })

      console.log("id", id, "records", this.records)

      if (!(id in this.records)) return

      // add all refs pointing to this object
      this.records[id].forEach((ci) => {
        const obj_id = ci.object_information.object_id
        console.log("create node for", obj_id)
        nodes.push({
          id: obj_id,
          label: ci.summary_line,
          shape: "icon", // "dot"
          icon: this.getIconCI(ci),
          size: 40,
       //   opacity: 0.7
        });

        edges.push({ from: obj_id, to: id, length: edgeLength, arrows: "to" });
      })
    }

    createNodes(this_ci)

    // nodes.push data of current item
    var data = {
      nodes: new DataSet(nodes), 
      edges: new DataSet(edges)
    };
    var options = {
      autoResize: true,
      height: "100%",
      width: "100%",
    };

    console.log("nodes", nodes);
    console.log("edges", edges);


    var network = new Network(target as HTMLElement, data, options);
    // this should be done on activating the tab
    network.fit()
  }


}
