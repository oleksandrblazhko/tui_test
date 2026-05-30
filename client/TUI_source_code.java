Приклади вже існуючого програмного коду клієнта для Processing

// ContinuousGestures.pde

void DO_setValue(int dataID, int ctrlID) {
  DataObject obj = DOlist.get(dataID);
  obj.setTempVal(map(degrees(obj.rotation-obj.prev_rotation), 0, 100, 0, 10));
}

void DO_setValueLoc2D(int dataID, int ctrlID) {
  DataObject obj = DOlist.get(dataID);
  TaggedObject b = tm.getBundle(ctrlID);
  if (b!=null) {
    PVector loc2D = img2screen(transformPoint(new PVector(b.tx, b.ty, b.tz), homography));
    obj.setTempVal(map(degrees(obj.rotation-obj.prev_rotation), 0, 100, 0, 10));
    obj.updateLoc2D(loc2D.x, loc2D.y);
  }
}

void DO_setLocOri2D(int dataID, int ctrlID) {
  DataObject obj = DOlist.get(dataID);
  TaggedObject b = tm.getBundle(ctrlID);
  if (b!=null) {
    PVector loc2D = img2screen(transformPoint(new PVector(b.tx, b.ty, b.tz), homography));
    obj.updateLoc2D(loc2D.x, loc2D.y);
    obj.updateOri2D(obj.rotation); //relative rotation (as a knob)
  }
}

// DataObject.pde

class DataObject {
  int OBJ_WIDTH = 300;
  int dataID;
  int lastCtrlID=-1;
  boolean multiControl;
  float x, y, rx, ry, rz, h, w;
  String name;
  float val;
  float tempVal = 0;
  ArrayList<Integer> ctrlIDList;
  ArrayList<PVector> ref2DList;
  ArrayList<Float> ref_rList;
  color fg_m = color(250, 177, 160);
  color fg_s = color(162, 155, 254);
  color bg = color(52);
  PVector ref2D; //reference 2D point for the MT gestures
  float ref_r; //reference angle for the MT gestures
  boolean bEngaged = false;
  float d0, theta0, theta_p;
  PVector m0;
  int textSizeL=24;
  int textSizeM=20;
  int gestureType = 0;
  int numTouches = 0;
  boolean gesturePerformed = false;
  final int UNDEFINED = 0;
  float scale = 1;
  float rotation = 0;
  float prev_rotation = 0;
  PVector translation = new PVector(0, 0);
  String lastGestureInfo = "";
  
  DataObject(int did, boolean multi, float val, float x, float y, float rx, float ry, float rz, float w, float h, String name) {
    this.dataID = did;
    this.set(val, x, y, rx, ry, rz, h, w);
    this.ref2D = new PVector(0, 0);
    this.ref_r = 0;
    this.ctrlIDList = new ArrayList<Integer>();
    this.ref2DList = new ArrayList<PVector>();
    this.ref_rList = new ArrayList<Float>();
    this.multiControl = multi;
    this.name = name;
  }

  DataObject(int did, boolean multi, float val, float x, float y, float rz, float w, float h, String name) {
    this.dataID = did;
    this.set(val, x, y, 0, 0, rz, h, w);
    this.ref2D = new PVector(0, 0);
    this.ref_r = 0;
    this.ctrlIDList = new ArrayList<Integer>();
    this.ref2DList = new ArrayList<PVector>();
    this.ref_rList = new ArrayList<Float>();
    this.multiControl = multi;
    this.name = name;
  }
  
  DataObject(int did, boolean multi, float val, float x, float y, float w, String name) {
    this.dataID = did;
    this.set(val, x, y, 0, 0, 0, w, w);
    this.ref2D = new PVector(0, 0);
    this.ref_r = 0;
    this.ctrlIDList = new ArrayList<Integer>();
    this.ref2DList = new ArrayList<PVector>();
    this.ref_rList = new ArrayList<Float>();
    this.multiControl = multi;
    this.name = name;
  }

  DataObject(int did, boolean multi, float val, float x, float y, String name) {
    this.dataID = did;
    this.set(val, x, y, 0, 0, 0, OBJ_WIDTH, OBJ_WIDTH);
    this.ref2D = new PVector(0, 0);
    this.ref_r = 0;
    this.ctrlIDList = new ArrayList<Integer>();
    this.ref2DList = new ArrayList<PVector>();
    this.ref_rList = new ArrayList<Float>();
    this.multiControl = multi;
    this.name = name;
  }

  void set(float val, float x, float y, float rx, float ry, float rz, float h, float w) {
    this.update(val, x, y, rx, ry, rz, h, w);
  }
  
  void setValue(float val){
    this.val = val;
  }
  void setTempVal(float val){
    this.tempVal = val;
  }

  void addCtrlID(int cid, PVector ref2d, float ref_r) {
    this.ctrlIDList.add(cid);
    this.ref2DList.add(ref2d);
    this.ref_rList.add(ref_r);
  }

  boolean hasCtrlID(int cid) {
    boolean found = false;
    for (int i : ctrlIDList) {
      if (i == cid) found=true;
    }
    return found;
  }
  
  void setPreviousRotation(float rz){
    prev_rotation = rz;
  }

  void removeCtrlID(int cid) {
    for (int i = ctrlIDList.size()-1; i>=0; i--) {
      if (this.ctrlIDList.get(i) == cid) {
        this.ctrlIDList.remove(i);
        this.ref2DList.remove(i);
        this.ref_rList.remove(i);
      }
    }
  }

  int getCtrlCounts() {
    return this.ctrlIDList.size();
  }

  void setRef2D(PVector l, float r) {
    this.ref2D = new PVector (l.x, l.y);
    this.ref_r = r;
  }
  
  void update(float val, float x, float y, float rx, float ry, float rz, float h, float w) {
    this.val = val;
    this.x = x;
    this.y = y;
    this.rx = rx;
    this.ry = ry;
    this.rz = rz;
    this.h = h;
    this.w = w;
  }

  void update(float val, float x, float y, float rz, float h, float w) {
    this.val = val;
    this.x = x;
    this.y = y;
    this.rz = rz;
    this.h = h;
    this.w = w;
  }

  void update(float val, float x, float y, float rz) {
    this.val = val;
    this.x = x;
    this.y = y;
    this.rz = rz;
  }

  void update(float val, float x, float y) {
    this.val = val;
    this.x = x;
    this.y = y;
  }

  void updateLoc2D(float x, float y) {
    this.x = x;
    this.y = y;
  }
  
  void updateOri2D(float rz) {
    this.rz = rz;
  }
  
  void updateOri3D(float rx,float ry, float rz) {
    this.rx = rx;
    this.ry = ry;
    this.rz = rz;
  }

  void update(float val) {
    this.val = val;
  }

  boolean checkHit(float cx, float cy, float d) {
    boolean hit = false;
    return abs(this.x-cx)<(this.w/2) && abs(this.y-cy)<(this.h/2);
  }

  void display() {
    drawDataObject();
  }
  
  void drawDataObject(){
    String ctrlIDstr = "";
    for (int i : ctrlIDList) ctrlIDstr += ("["+i+"]");
    String label = dataID+":"+ctrlIDstr+"\n"+nf((val+tempVal),0,2);
    pushMatrix();
    pushStyle();
    if(multiControl) fill(fg_m);
    else fill(fg_s);
    noStroke();
    rectMode(CENTER);
    rect(x,y, w, w);
    fill(bg);
    noStroke();
    textSize(w/6);
    textAlign(CENTER, CENTER);
    text(label, x, y);
    popStyle();
    popMatrix();
  }
  
  void drawSTGestureInfo() {
    String info = "[Thresholds > Movement]\n" + 
      "\n rotation =" + nf(degrees(rotation), 1, 2) +
      "\n translation = (X: " + nf(translation.x, 1, 1) + ", Y:" + nf(translation.y, 1, 1) + ")";
    if (gestureType!=UNDEFINED) {
      info ="[Movement > Thresholds]\n rotation = " + nf(degrees(rotation), 1, 2) + " degrees \n" +
        "translation = (X: " + nf(translation.x, 1, 1) + ", Y:" + nf(translation.y, 1, 1) + ") pixels";
    }
    pushStyle();
    fill(0, 255, 0);
    textSize(textSizeM);
    text(info, this.x, this.y);
    rectMode(CENTER);
    noFill();
    popStyle();
  }
  
  void getSTGestureType() {
    //if (gestureType==UNDEFINED) {
    //  dataObjectIsSingleTapped(dataID, lastCtrlID);
    //}
  }
  
  void drawSTGestureType() {
    pushMatrix();
    pushStyle();
    fill(0, 255, 0);
    textSize(textSizeM);
    translate(this.x,this.y);
    String lastGestureInfo =" rotated " + nf(degrees(this.rotation), 1, 2) + " degrees" +
      "\n translated (X: " + nf(this.translation.x, 1, 1) + ", Y:" + nf(this.translation.y, 1, 1) + ") pxs";
    text("last gesture:\n"+ lastGestureInfo, 0, 0);
    //text("Can be recognized as:", 0, 3*textSizeL);
    //if (gestureType==UNDEFINED && numTouches>0) {
    //  text(dataID+":[tapped]", 0, 5*textSizeL);
    //}
    popStyle();
    popMatrix();
  }
  
}

// Tag.pde

class Tag {
  int TTL = 200; //adjust this number to alter sensitivity (unit: ms)
  boolean active;
  long ts;
  int id;
  float tx, ty, tz, rx, ry, rz;
  PVector[] corners;

  Tag(int id) {
    this.id = id;
    this.tx = 0;
    this.ty = 0;
    this.tz = 0;
    this.rx = 0;
    this.ry = 0;
    this.rz = 0;
    this.corners = new PVector[4];
    this.ts = 0;
    this.active = false;
  }

  void checkActive() {
    if (this.active && (millis()-this.ts)>this.TTL) {
      this.active = false;
      Tag_Absent3D(this.id, this.tx, this.ty, this.tz, this.rx, this.ry, this.rz);
    }
  }

  void set(float tx, float ty, float tz, float rx, float ry, float rz, PVector[] corners) {
    this.ts = millis();
    this.tx = tx;
    this.ty = ty;
    this.tz = tz;
    this.rx = rx;
    this.ry = ry;
    this.rz = rz;
    this.corners = corners;
    if (!this.active){
      Tag_Present3D(this.id, this.tx, this.ty, this.tz, this.rx, this.ry, this.rz);
    }else{
      Tag_Update3D(this.id, this.tx, this.ty, this.tz, this.rx, this.ry, this.rz);
    }
    this.active = true;
  }
}

// TagManager.pde

class TagManager {
  int TAG_D = 150;
  int TO_D = 150;
  Tag[] tags;
  ArrayList<TaggedObject> taggedObjects;
  PMatrix3D R1;
  PMatrix3D R2;
  ArrayList<Integer> activeTags;
  ArrayList<Integer> activeTOs;

  TagManager(int n, ArrayList to_ids, ArrayList to_offs) {
    tags = new Tag[n];
    this.taggedObjects = new ArrayList<TaggedObject>();
    activeTags = new ArrayList<Integer>();
    activeTOs = new ArrayList<Integer>();
    for (int i = 0; i < n; i++) {
      tags[i] = new Tag(i);
    }
    for (int i = 0; i < to_ids.size(); i++) {
      ArrayList<Integer> ids = (ArrayList<Integer>) to_ids.get(i);
      ArrayList<PVector> offs = (ArrayList<PVector>) to_offs.get(i);
      this.taggedObjects.add(new TaggedObject(ids, offs));
    }
  }

  void set(int id, float tx, float ty, float tz, float rx, float ry, float rz, PVector[] corners) {
    tags[id].set(tx, ty, tz, rx, ry, rz, corners);
  }

  void update() {
    activeTags.clear();
    activeTOs.clear();
    for (Tag t : this.tags) {
      t.checkActive();
      if (t.active) activeTags.add(t.id);
    }
    if (homographyMatrixCalculated) {
      for (TaggedObject _to : this.taggedObjects) {
        ArrayList<Tag> activeTags = new ArrayList<Tag>();
        for (Integer id : _to.ids) {
          if (tags[id].active) {
            activeTags.add(tags[id]);
          }
        }
        if (activeTags.size() > 0) {
          PVector loc = new PVector(0, 0, 0);
          PVector ori = new PVector(0, 0, 0);

          for (Tag t : activeTags) {
            PVector O = new PVector(t.tx, t.ty, t.tz);
            PVector offset = _to.getOffsetFromID(t.id);
            PVector v = new PVector(0, 0, offset.z);
            R1 = new PMatrix3D();
            R1.rotateZ(-t.rz);
            R1.rotateX(t.rx);
            R1.rotateY(t.ry);
            R1.rotateZ(t.rz);
            PVector rotated_v = new PVector();
            R1.mult(v, rotated_v);
            PVector P = new PVector(O.x - rotated_v.x, O.y + rotated_v.y, O.z + rotated_v.z); // x is inversed because of the inversed coordinate

            PVector w = new PVector(offset.x, offset.y, 0);
            R2 = new PMatrix3D();
            R2.rotateX(t.rx);
            R2.rotateY(t.ry);
            R2.rotateZ(t.rz);
            PVector rotated_w = new PVector();
            R2.mult(w, rotated_w);
            PVector P_prime = new PVector(P.x - rotated_w.x, P.y + rotated_w.y, P.z + rotated_w.z); // x is inversed because of the inversed coordinate
            loc.add(new PVector(P_prime.x, P_prime.y, P_prime.z));
            ori.add(new PVector(t.rx, t.ry, t.rz));
          }

          loc.div(activeTags.size());
          ori.div(activeTags.size());
          _to.set(loc.x, loc.y, loc.z, ori.x, ori.y, ori.z);
        } else {
          _to.setInactive();
        }
      }
      int i = 0;
      for (TaggedObject _to : this.taggedObjects) {
        if (_to.active) activeTOs.add(i);
        i++;
      }
    }
  }

  void displayRaw() {
    for (Tag t : tags) {
      if (t.active) {
        pushMatrix();
        pushStyle();
        noStroke();
        fill(255, 0, 0);
        ellipse(t.corners[0].x, t.corners[0].y, 5, 5);
        fill(255, 255, 0);
        ellipse(t.corners[1].x, t.corners[1].y, 5, 5);
        fill(0, 255, 255);
        ellipse(t.corners[2].x, t.corners[2].y, 5, 5);
        fill(0, 0, 255);
        ellipse(t.corners[3].x, t.corners[3].y, 5, 5);
        fill(0, 0, 255);


        beginShape();
        fill(255);
        stroke(0, 255, 0);
        for (int i = 0; i < 4; i++) {
          vertex(t.corners[i].x, t.corners[i].y);
        }
        endShape(CLOSE);

        fill(52);
        noStroke();

        PVector c = new PVector((t.corners[0].x+t.corners[2].x)/2, (t.corners[0].y+t.corners[2].y)/2);
        String s = "(x,y)=("+nf(round(t.tx*100))+","+nf(round(t.ty*100))+")\nz="+nf(round(t.tz*100));
        textAlign(CENTER, CENTER);
        textSize(18);
        text("ID="+t.id+"\n"+s, c.x, c.y);
        popStyle();
        popMatrix();
      }
    }
  }
  
  ArrayList<TaggedObject> getActiveTOs() {
    ArrayList<TaggedObject> list = new ArrayList<TaggedObject>();
    for (int to_id : activeTOs) list.add(taggedObjects.get(to_id));
    return list;
  }

  TaggedObject getBundle(int to_id) {
    TaggedObject to_x = null;
    ArrayList<TaggedObject> list = getActiveTOs();
    for (int i=0; i<list.size(); i++) {
      TaggedObject _to = list.get(i);
      for (int id : _to.ids) if (to_id==id) to_x=_to;
    }
    return to_x;
  }

  ArrayList<Tag> getActiveTags() {
    ArrayList<Tag> list = new ArrayList<Tag>();
    for (int tid : activeTags) list.add(tags[tid]);
    return list;
  }

  void drawActiveTOs(SimpleMatrix homography) {
    for (TaggedObject _to : getActiveTOs()) {
      float toD = TO_D;
      float angle2D = _to.rz-global_rz;
      //PVector tilt2D = new PVector(b.rx-global_rx,b.ry-global_ry);
      PVector tilt2D = new PVector(0, 0);
      PVector loc2D = img2screen(transformPoint(new PVector(_to.tx, _to.ty, _to.tz), homography));
      float distance = distancePointToPlane(new PVector(_to.tx, _to.ty, _to.tz), planePoints);
      if (distance<touchThreshold){ 
        drawTagSimple(_to.ids.get(0), loc2D, angle2D, tilt2D, toD, color(0, 127, 255, 52)); //example visualization
      }else{ 
        drawTagSimple(_to.ids.get(0), loc2D, angle2D, tilt2D, toD, color(0, 127, 255, 0)); //example visualization
      }
    }
  }
  
  void drawCustomActiveBundles(SimpleMatrix homography) {
    for (TaggedObject _to : getActiveTOs()) {
      float toD = TO_D;
      float angle2D = _to.rz-global_rz;
      //PVector tilt2D = new PVector(b.rx-global_rx,b.ry-global_ry);
      PVector tilt2D = new PVector(0, 0);
      PVector loc2D = img2screen(transformPoint(new PVector(_to.tx, _to.ty, _to.tz), homography));
      float distance = distancePointToPlane(new PVector(_to.tx, _to.ty, _to.tz), planePoints);
      if (distance<touchThreshold){ 
        drawTagCustom(_to.ids.get(0), loc2D, angle2D);
      }
    }
  }

  void drawActiveTags(SimpleMatrix homography) {
    for (Tag t : getActiveTags()) {
      if (!isCorner(t.id) && t.id !=0) {
        float tagD = TAG_D;
        float angle2D = t.rz-global_rz;
        //PVector tilt2D = new PVector(t.rx-global_rx,t.ry-global_ry);
        PVector tilt2D = new PVector(0, 0);
        PVector loc2D = img2screen(transformPoint(new PVector(t.tx, t.ty, t.tz), homography));
        float distance = distancePointToPlane(new PVector(t.tx, t.ty, t.tz), planePoints);
        if (distance<touchThreshold) drawTagSimple(t.id, loc2D, angle2D, tilt2D, tagD, color(100)); //example visualization
        else drawTagSimple(t.id, loc2D, angle2D, tilt2D, tagD, color(100, 100));
      }
    }
  }

  void drawTagSimple(int id, PVector loc2D, float angle2D, PVector tilt2D, float D, color c) {
    float R = D/2;
    if (R>=1) {
      pushMatrix();
      pushStyle();
      fill(c);
      strokeWeight(5);
      stroke(0);
      ellipse(loc2D.x, loc2D.y, D, D);
      line(loc2D.x, loc2D.y, loc2D.x + R * (cos(angle2D)), loc2D.y + R * (sin(angle2D)));
      //noFill();
      //ellipse(loc2D.x+R*sin(tilt2D.x), loc2D.y+R*sin(tilt2D.y), R, R);
      fill(255);
      noStroke();
      textSize(R);
      textAlign(CENTER, CENTER);
      text(id, loc2D.x, loc2D.y);
      fill(0);
      noStroke();
      textSize(R/3);
      textAlign(RIGHT, BOTTOM);
      text(id, loc2D.x+R, loc2D.y+R);
      popStyle();
      popMatrix();
    }
  }

  void drawTagCustom(int id, PVector loc2D, float angle2D) {
    int tagID = id;
    int R = 50;
    pushMatrix();
    pushStyle();
    fill(52);
    strokeWeight(5);
    stroke(0);
    ellipse(loc2D.x, loc2D.y, R*2, R*2);
    noStroke();
    ellipse(loc2D.x + R * (cos(angle2D)), loc2D.y + R * (sin(angle2D)), R/2, R/2);
    fill(255);
    noStroke();
    textSize(R/2);
    textAlign(CENTER, CENTER);
    text(id, loc2D.x-R, loc2D.y-R);
    popStyle();
    popMatrix();
  }
}

// TaggedObject.pde

class TaggedObject {
  int TTL = 100;
  boolean active;
  long ts;
  ArrayList<Integer> ids;
  ArrayList<PVector> offs;
  float tx, ty, tz, rx, ry, rz;
  float p_rx, p_ry, p_rz;

  TaggedObject(ArrayList<Integer> TO_IDs, ArrayList<PVector> IDoffsets) {
    this.ids = new ArrayList<Integer>();
    this.offs = new ArrayList<PVector>();
    for (int i = 0; i < TO_IDs.size(); i++) {
      this.ids.add(TO_IDs.get(i));
      this.offs.add(IDoffsets.get(i));
    }
    this.tx = 0;
    this.ty = 0;
    this.tz = 0;
    this.rx = 0;
    this.ry = 0;
    this.rz = 0;
    this.ts = 0;
    this.active = false;
  }

  void setInactive() {
    if (this.active && (millis()-this.ts)>this.TTL) {
      this.active = false;
      TO_Absent2D(this.getTO_ID(), this.tx, this.ty, this.tz, this.rz);
    }
  }

  float unwrapAngle(float currentAngle, float previousAngle) {
    float deltaAngle = currentAngle - previousAngle;
    if (deltaAngle > PI) {
      currentAngle -= TWO_PI;
    } else if (deltaAngle < -PI) {
      currentAngle += TWO_PI;
    }
    return currentAngle;
  }

  void set(float tx, float ty, float tz, float rx, float ry, float rz) {
    boolean update = true;
    this.tx = tx;
    this.ty = ty;
    this.tz = tz;
    this.rx = unwrapAngle(rx, p_rx);
    this.ry = unwrapAngle(ry, p_ry);
    this.rz = unwrapAngle(rz, p_rz);
    
    float distance = distancePointToPlane(new PVector(tx, ty, tz), planePoints);
    if (distance<touchThreshold) {
      if (!this.active) {
        TO_Present2D(this.getTO_ID(), this.tx, this.ty, this.tz, this.rz);
      } else {
        TO_Update2D(this.getTO_ID(), this.tx, this.ty, this.tz, this.rz);
      }
      this.active = true;
      this.ts = millis();
    } else {
      if (this.active && (millis()-this.ts)>this.TTL) {
        this.active = false;
        TO_Absent2D(this.getTO_ID(), this.tx, this.ty, this.tz, this.rz);
      }
    }
  }

  int getTO_ID() {
    return this.ids.get(0);
  }

  PVector getScreenLoc2D(SimpleMatrix homography) {
    return img2screen(transformPoint(new PVector(this.tx, this.ty, this.tz), homography));
  }

  PVector getOffsetFromID (int targetID) {
    int index = -1;
    for (int i = 0; i < this.ids.size(); i++) {
      if (this.ids.get(i) == targetID) {
        index = i;
        break;
      }
    }
    if (index>=0) return this.offs.get(index);
    else return new PVector(0, 0, 0);
  }
}

// oscEvent.pde

void oscEvent(OscMessage msg) {
  if (msg.checkAddrPattern("/marker")) {
    int id = msg.get(0).intValue();
    float tx = msg.get(1).floatValue();
    float ty = msg.get(2).floatValue();
    float tz = msg.get(3).floatValue();
    float rx = msg.get(4).floatValue();
    float ry = msg.get(5).floatValue();
    float rz = msg.get(6).floatValue();
    float p1x = msg.get(7).intValue();
    float p1y = msg.get(8).intValue();
    float p2x = msg.get(9).intValue();
    float p2y = msg.get(10).intValue();
    float p3x = msg.get(11).intValue();
    float p3y = msg.get(12).intValue();
    float p4x = msg.get(13).intValue();
    float p4y = msg.get(14).intValue();
    PVector[] corners = {new PVector(p1x,p1y),new PVector(p2x,p2y),new PVector(p3x,p3y),new PVector(p4x,p4y)};
    tm.set(id, tx, ty, tz, rx, ry, rz, corners);
  }
}

// API.pde

//Event listeners
void Tag_Present3D(int id, float tx, float ty, float tz, float rx, float ry, float rz) {
    if (serialDebug && id!=0) println("+ Tag:", id, "loc = (", tx, ",", ty, ",", tz, "), angle = (", degrees(rx),",",degrees(ry),",",degrees(rz),")");
}

void Tag_Absent3D(int id, float tx, float ty, float tz, float rx, float ry, float rz) {
    if (serialDebug && id!=0) println("- Tag:", id, "loc = (", tx, ",", ty, ",", tz,"), angle = (", degrees(rx),",",degrees(ry),",",degrees(rz),")");
}

void Tag_Update3D(int id, float tx, float ty, float tz, float rx, float ry, float rz) {
    if (serialDebug &&id!=0) println("% Tag:", id, "loc = (", tx, ",", ty, ",", tz,"), angle = (", degrees(rx),",",degrees(ry),",",degrees(rz),")");
}

//added in Lab2
void TO_Present2D(int id, float x, float y, float z, float rz) {
  if (serialDebug && homographyMatrixCalculated && !isCorner(id)) {
    PVector t = img2screen(transformPoint(new PVector(x, y, z), homography));
    println("+ Bundle:", id, "loc = (", t.x, ",", t.y, "), angle = ", degrees(rz));
  }
  if (homographyMatrixCalculated && !isCorner(id)) {
    PVector t = img2screen(transformPoint(new PVector(x, y, z), homography));
    for (DataObject obj : DOlist) {
      if (obj.checkHit(t.x, t.y, tm.TO_D/2)) {
        if (!obj.hasCtrlID(id)) {
          obj.addCtrlID(id, new PVector(t.x,t.y), rz);
        }
      }
    }
  }
}

void TO_Absent2D(int id, float x, float y, float z, float rz) {
  if (serialDebug && homographyMatrixCalculated && !isCorner(id)) {
    PVector t = img2screen(transformPoint(new PVector(x, y, z), homography));
    println("- Bundle:", id, "loc = (", t.x, ",", t.y, "), angle = ", degrees(rz));
  }
  if (homographyMatrixCalculated && !isCorner(id)) {
    PVector t = img2screen(transformPoint(new PVector(x, y, z), homography));
    for (DataObject obj : DOlist) {
      if (obj.hasCtrlID(id)) {
        obj.setPreviousRotation(obj.rotation);
        obj.removeCtrlID(id);
      }
    }
  }
}

void TO_Update2D(int id, float x, float y, float z, float rz) {
  if (serialDebug && homographyMatrixCalculated && !isCorner(id)) {
    PVector t = img2screen(transformPoint(new PVector(x, y, z), homography));
    println("- Bundle:", id, "loc = (", t.x, ",", t.y, "), angle = ", degrees(rz));
  }
  if (homographyMatrixCalculated && !isCorner(id)) {
    PVector t = img2screen(transformPoint(new PVector(x, y, z), homography));
    for (DataObject obj : DOlist) {
      if (obj.hasCtrlID(id)) {
        
      }
    }
  }
}

// tools.pde

boolean resetData = false;
boolean gestureDebug = false;
boolean dataObjectDebug = false;
boolean tagDebug = false;
boolean serialDebug = false;

PVector[] srcPointsT = new PVector[4];
PVector[] dstPointsT = new PVector[4];
PVector[] srcPointsR = new PVector[4];
PVector[] dstPointsR = new PVector[4];
PVector[] planePoints = new PVector[4];

boolean homographyMatrixCalculated = false;
SimpleMatrix homography;

ArrayList idTOs;
ArrayList offsetTOs;
PImage calibImg; //the calibration image
int[] cornersID = {1, 3, 2, 0}; //the corner markers of the calibration image. only the first three are used.
float tag2screenRatio = 297. / paperWidthOnScreen; //1
PVector cCen = new PVector (842./2., 595./2.);
float mW = (markerWidth/25.4*72.)*tag2screenRatio;
float calibgridWidth = 100+markerWidth; //unit:mm
float calibgridHeight = 100+markerWidth; //unit:mm
float mDC1 = (calibgridWidth/2)*(72/25.4)*tag2screenRatio;
float mDC2 = (calibgridHeight/2)*(72/25.4)*tag2screenRatio;
float[] markerX = {(cCen.x-mDC1+mW/2), (cCen.x-mDC1+mW/2), (cCen.x+mDC2-mW/2), (cCen.x+mDC2-mW/2)};
float[] markerY = {(cCen.y-mDC1+mW/2), (cCen.y+mDC1+mW/2), (cCen.y-mDC2-mW/2), (cCen.y+mDC2-mW/2)};
float markerGridWidth = markerX[2]-markerX[0];
PVector markerOffset = new PVector(markerX[0], markerY[0]);
PVector windowOffset = new PVector(0, 0);
PVector imageOffset = new PVector(0, 0);
float global_rx=0;
float global_ry=0;
float global_rz=0;
float alpha = 0;

boolean drawing = false; //when token does not hit the dataobject, set drawMode as true

void initTagManager() {
  idTOs = new ArrayList();
  offsetTOs = new ArrayList();
  for (int i = 0; i < TO_IDs.length; i++) {
    ArrayList ids = new ArrayList();
    ArrayList offsets = new ArrayList();
    for (int j = 0; j < TO_IDs[i].length; j++) {
      ids.add(TO_IDs[i][j]);
      offsets.add(TO_Offsets[i][j]);
    }
    idTOs.add(ids);
    offsetTOs.add(offsets);
  }
  tm = new TagManager(600, idTOs, offsetTOs);
}

void loadCalibrationImg(String s) {
  calibImg = loadImage(s); //select the calibration image
  imageOffset.set((width - calibImg.width)/2, (height - calibImg.height)/2); //center the calibration image
}

void loadCalibrationFile(String filename) {
  String[] lines;
  try {
    lines = loadStrings(filename);
    if (lines == null) {
      throw new RuntimeException("File not found: srcPoints.txt");
    }
    // Initialize and parse srcPoints
    PVector[] cornerPointsT = new PVector[lines.length];
    PVector[] cornerPointsR = new PVector[lines.length];
    for (int i = 0; i < lines.length; i++) {
      String[] coords = split(lines[i], ",");
      float tx = float(trim(coords[0]));
      float ty = float(trim(coords[1]));
      float tz = float(trim(coords[2]));
      float rx = float(trim(coords[3]));
      float ry = float(trim(coords[4]));
      float rz = float(trim(coords[5]));
      cornerPointsT[i] = new PVector(tx, ty, tz);
      cornerPointsR[i] = new PVector(rx, ry, rz);
      println(tx, ty, tz, rx, ry, rz);
    }
    calculateHomographyMatrix(cornerPointsT); //calculate the homography matrix
    registerPlanePoints(); //register the plane points for plane calculation.
    registerPlaneOrientation(cornerPointsR); //register the plane orientation for plane calculation.
    homographyMatrixCalculated = true; //set the homography matrix flag to "calculated"
  }
  catch (Exception e) {
    println("Error loading file: " + e.getMessage());
  }
}

void saveCalibrationFile(String filename) {
  srcPointsT[0] = new PVector(tm.tags[cornersID[0]].tx, tm.tags[cornersID[0]].ty, tm.tags[cornersID[0]].tz);
  srcPointsT[1] = new PVector(tm.tags[cornersID[1]].tx, tm.tags[cornersID[1]].ty, tm.tags[cornersID[1]].tz);
  srcPointsT[2] = new PVector(tm.tags[cornersID[2]].tx, tm.tags[cornersID[2]].ty, tm.tags[cornersID[2]].tz);
  srcPointsR[0] = new PVector(tm.tags[cornersID[0]].rx, tm.tags[cornersID[0]].ry, tm.tags[cornersID[0]].rz);
  srcPointsR[1] = new PVector(tm.tags[cornersID[1]].rx, tm.tags[cornersID[1]].ry, tm.tags[cornersID[1]].rz);
  srcPointsR[2] = new PVector(tm.tags[cornersID[2]].rx, tm.tags[cornersID[2]].ry, tm.tags[cornersID[2]].rz);
  String[] lines = new String[3];
  for (int i = 0; i < 3; i++) {
    lines[i] = nf((float)srcPointsT[i].x, 0, 3) + ", " + nf((float)srcPointsT[i].y, 0, 3) + ", " + nf((float)srcPointsT[i].z, 0, 3)+ ", " +
               nf((float)srcPointsR[i].x, 0, 3) + ", " + nf((float)srcPointsR[i].y, 0, 3) + ", " + nf((float)srcPointsR[i].z, 0, 3);
    println(lines[i]);
  }
  saveStrings("corners.txt", lines);
}
void calculateHomographyMatrix(PVector[] cornerPointsT) {
  srcPointsT[0] = new PVector(cornerPointsT[0].x, cornerPointsT[0].y, cornerPointsT[0].z);
  srcPointsT[1] = new PVector(cornerPointsT[1].x, cornerPointsT[1].y, cornerPointsT[1].z);
  srcPointsT[2] = new PVector(cornerPointsT[2].x, cornerPointsT[2].y, cornerPointsT[2].z);

  dstPointsT[0] = new PVector(0, 0);
  dstPointsT[1] = new PVector(1, 0);
  dstPointsT[2] = new PVector(1, 1);

  homography = calculateHomography(srcPointsT, dstPointsT);
}


void calculateHomographyMatrix() {
  srcPointsT[0] = new PVector(tm.tags[cornersID[0]].tx, tm.tags[cornersID[0]].ty, tm.tags[cornersID[0]].tz);
  srcPointsT[1] = new PVector(tm.tags[cornersID[1]].tx, tm.tags[cornersID[1]].ty, tm.tags[cornersID[1]].tz);
  srcPointsT[2] = new PVector(tm.tags[cornersID[2]].tx, tm.tags[cornersID[2]].ty, tm.tags[cornersID[2]].tz);

  dstPointsT[0] = new PVector(0, 0);
  dstPointsT[1] = new PVector(1, 0);
  dstPointsT[2] = new PVector(1, 1);
  
  homography = calculateHomography(srcPointsT, dstPointsT);
}

void registerPlanePoints() {
  planePoints[0] = new PVector(srcPointsT[0].x, srcPointsT[0].y, srcPointsT[0].z);
  planePoints[1] = new PVector(srcPointsT[1].x, srcPointsT[1].y, srcPointsT[1].z);
  planePoints[2] = new PVector(srcPointsT[2].x, srcPointsT[2].y, srcPointsT[2].z);
}

void registerPlaneOrientation(){
  global_rx= (tm.tags[cornersID[0]].rx + tm.tags[cornersID[1]].rx + tm.tags[cornersID[2]].rx)/3;
  global_ry= (tm.tags[cornersID[0]].ry + tm.tags[cornersID[1]].ry + tm.tags[cornersID[2]].ry)/3;
  global_rz= (tm.tags[cornersID[0]].rz + tm.tags[cornersID[1]].rz + tm.tags[cornersID[2]].rz)/3;
  println(global_rx,global_ry,global_rz);
}

void registerPlaneOrientation(PVector[] cornerPointsR){
  global_rx= (cornerPointsR[0].x + cornerPointsR[1].x + cornerPointsR[2].x)/3;
  global_ry= (cornerPointsR[0].y + cornerPointsR[1].y + cornerPointsR[2].y)/3;
  global_rz= (cornerPointsR[0].z + cornerPointsR[1].z + cornerPointsR[2].z)/3;
  println(global_rx,global_ry,global_rz);
}

boolean cornersDetected() {
  if (tm.tags[cornersID[0]].active &&
    tm.tags[cornersID[1]].active &&
    tm.tags[cornersID[2]].active) {
    return true;
  } else {
    return false;
  }
}

boolean isCorner(int id) {
  if (id == cornersID[0] || id == cornersID[1] || id == cornersID[2]) {
    return true;
  } else {
    return false;
  }
}

SimpleMatrix calculateHomography(PVector[] srcPoints, PVector[] dstPoints) {
  SimpleMatrix srcMatrix = new SimpleMatrix(3, 3);
  SimpleMatrix dstMatrix = new SimpleMatrix(3, 3);

  for (int i = 0; i < 3; i++) {
    srcMatrix.set(0, i, srcPoints[i].x);
    srcMatrix.set(1, i, srcPoints[i].y);
    srcMatrix.set(2, i, srcPoints[i].z);

    dstMatrix.set(0, i, dstPoints[i].x);
    dstMatrix.set(1, i, dstPoints[i].y);
    dstMatrix.set(2, i, 1.0);
  }

  return dstMatrix.mult(srcMatrix.pseudoInverse());
}

PVector transformPoint(PVector point, SimpleMatrix homography) {
  float x = point.x;
  float y = point.y;
  float z = point.z;

  SimpleMatrix result = homography.mult(new SimpleMatrix(new double[][] {{x}, {y}, {z}}));

  float w = (float) result.get(2, 0);
  float transformedX = (float) (result.get(0, 0) / w);
  float transformedY = (float) (result.get(1, 0) / w);

  return new PVector(transformedX, transformedY);
}

PVector img2screen(PVector p) {
  PVector wo = windowOffset;
  PVector io = imageOffset;
  PVector mo = markerOffset;
  float mgw = markerGridWidth;
  return new PVector (p.x*mgw + wo.x + io.x + mo.x, p.y*mgw + wo.y + io.y + mo.y);
}

float distancePointToPlane(PVector point, PVector[] planePoints) {
  PVector normal = cross(subtract(planePoints[1], planePoints[0]), subtract(planePoints[2], planePoints[0])); // Calculate the normal vector to the plane
  float d = -dot(normal, planePoints[0]); // Calculate the d coefficient of the plane equation

  // Use the plane equation to find the distance
  float numerator = abs(dot(normal, point) + d);
  float denominator = sqrt(pow(normal.x, 2) + pow(normal.y, 2) + pow(normal.z, 2));

  return numerator / denominator;
}

PVector cross(PVector v1, PVector v2) {
  return new PVector(
    v1.y * v2.z - v1.z * v2.y,
    v1.z * v2.x - v1.x * v2.z,
    v1.x * v2.y - v1.y * v2.x
    );
}

float dot(PVector v1, PVector v2) {
  return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;
}

PVector subtract(PVector v1, PVector v2) {
  return new PVector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z);
}

float getDistanceBetween(PVector p0, PVector p1) {
  return dist(p0.x, p0.y, p1.x, p1.y);
}

float getAngleBetween(PVector p0, PVector p1) {
  return atan2(p1.y-p0.y, p1.x-p0.x);
}

PVector getCentroidBetween(PVector p0, PVector p1) {
  return PVector.add(p0, p1).div(2);
}

int whichTO(int id) {
  for (int i = 0; i < TO_IDs.length; i++) {
    if (TO_IDs[i][0] == id) {
      return i;  // Return the index where the ID matches
    }
  }
  return -1;  // Return -1 if the ID is not found
}

float mmToPx (float mm){
  return mm * (72. / 25.4)*tag2screenRatio;
}

PVector getTiltAngles(PVector tilt2D, float angle2D) {
  PVector obj = new PVector(global_rx, global_ry, global_rz);
  PVector surf = new PVector(tilt2D.x, tilt2D.y, angle2D);
  // 1. Generate Rotation Matrices for both
  PMatrix3D R_s = getRotationMatrix(surf.x, surf.y, surf.z);
  PMatrix3D R_o = getRotationMatrix(obj.x, obj.y, obj.z);
  // 2. Get Relative Rotation: R_rel = (R_s^T) * R_o
  // In rotation matrices, the Transpose is the Inverse.
  R_s.transpose();
  PMatrix3D R_rel = new PMatrix3D();
  R_rel.set(R_s);
  R_rel.apply(R_o);
  float tilt_X = atan2(R_rel.m21, R_rel.m22);
  float tilt_Y = atan2(-R_rel.m20, sqrt(sq(R_rel.m21) + sq(R_rel.m22)));
  float relRoll = atan2(R_rel.m10, R_rel.m00);

  PVector results = new PVector(tilt_X, -tilt_Y, relRoll);
  return results;
}

PMatrix3D getRotationMatrix(float roll, float pitch, float yaw) {
  PMatrix3D mat = new PMatrix3D();
  // Standard ZYX order: Yaw (Z), then Pitch (Y), then Roll (X)
  mat.rotateZ(yaw);
  mat.rotateY(pitch);
  mat.rotateX(roll);
  return mat;
}

// ArUcoTUI_Client.pde

//*********************************************
// Example Code: ArUco-TUI Client v26.1
// ArUCo Fiducial Marker Detection in OpenCV Python and then send to Processing via OSC
// Tracking Tangibles on a Surface or Flat Panel Display with 15mm-width Markers
// Rong-Hao Liang: r.liang@tue.nl
//*********************************************

import oscP5.*;
import netP5.*;
import processing.net.*;

TagManager tm;
OscP5 oscP5;
////set the TO IDs and offsets (unit: m)
int[][] TO_IDs = {{48}, {49}, {50}, {51}};
PVector[][] TO_Offsets = {{new PVector(0, 0, -0.025)}, {new PVector(0, 0, -0.025)}, {new PVector(0, 0, -0.025)}, {new PVector(0, 0, -0.025)}};
////set the paper width on screen (initial value: 297; unit mm)
//float paperWidthOnScreen = 297; //First measure the real-world size of the clibration sheet.
float paperWidthOnScreen = 193.5; //After measurement, change this parameter. 
////set the marker width on screen
float markerWidth = 15; //(mm) change this if the marker is of a different width
////set the touch threshold (unit: m)
float touchThreshold = 0.01; //change this to adjust sensitivity of touch sensing.

ArrayList<DataObject> DOlist = new ArrayList<DataObject>(); //the data objects

int gestureMode = 2; //try 1 to 3.

void initDataObjects() { //set up the data objects
  float dataObjSize = 200;
  DOlist.add(new DataObject(0, false, 10, width/2-dataObjSize, height/2-dataObjSize, dataObjSize, "Obj. 1"));
  DOlist.add(new DataObject(1, false, 10, width/2+dataObjSize, height/2-dataObjSize, dataObjSize, "Obj. 2"));
  DOlist.add(new DataObject(2, false, 10, width/2-dataObjSize, height/2+dataObjSize, dataObjSize, "Obj. 3"));
  DOlist.add(new DataObject(3, false, 10, width/2+dataObjSize, height/2+dataObjSize, dataObjSize, "Obj. 4"));
}

void setup() {
  size(1280, 720); //initialize canvas
  oscP5 = new OscP5(this, 9000); //initialize OSC connection via port 9000
  loadCalibrationImg("ArUco_Grid15.png"); //load calibration image
  initTagManager(); //initialize tag manager
  initDataObjects(); //initialize the data objects.
  loadCalibrationFile("corners.txt");
}

void draw() {
  tm.update(); //update the tag manager and the states of tags.
  if (!homographyMatrixCalculated) { //if the homography matrix has not been calculated
    background(200);
    drawCalibImage(); //draw the calibration image
    if (cornersDetected()) { //when the corner markers are detected
      calculateHomographyMatrix(); //calculate the homography matrix
      registerPlanePoints(); //register the plane points for plane calculation.
      registerPlaneOrientation(); //register the plane orientation for plane calculation.
      saveCalibrationFile("corners.txt");
      homographyMatrixCalculated = true; //set the homography matrix flag to "calculated"
    }
  } else {
    background(100);
    updateAllDataObjects(gestureMode); //update the state of data objects
    displayUI(gestureMode); //display the UI without debugging message.
    tm.drawActiveTOs(homography);  //draw the computed bundle locations in 2D
    showDebuggers();////for debugging
  }
}

void displayCustomUI() {
  //make your own visualization
  for (DataObject obj : DOlist) {
    int dataID = obj.dataID;
    int value = (int)(obj.val+obj.tempVal);
    pushMatrix();
    fill(52);
    pushStyle();
    rectMode(CENTER);
    pushMatrix();
    translate(obj.x, obj.y);
    rotate(obj.rz);
    rect(0, 0, obj.w, obj.h);
    popMatrix();
    fill(52);
    textSize(0);
    text(value, obj.x, obj.y);
    popMatrix();
  }
}

void resetDataObjects() {
  DOlist.clear();
  initDataObjects();
  resetData = false;
}

void showDebuggers() {
  if (dataObjectDebug) displayDataObjects(); //display the debugging message of data objects
  if (gestureDebug) drawAllGestures(); //display the debugging messages of gestures
  if (tagDebug) tm.drawActiveTags(homography);  //draw the computed bundle locations in 2D
}

void displayDataObjects() {
  for (DataObject obj : DOlist) {
    obj.display();
  }
}

void displayUI(int output_mode) {
  for (DataObject obj : DOlist) {
    String value = nf((int)(obj.val+obj.tempVal), 0, 0);
    String label = "("+obj.dataID+")"+obj.name+":"+value;
    if(obj.lastCtrlID>=0) label += " <- "+ obj.lastCtrlID;
    pushMatrix();
    pushStyle();
    rectMode(CENTER);
    noStroke();
    if (!obj.multiControl) fill(250, 177, 160);
    else fill(162, 155, 254);
    pushMatrix();
    translate(obj.x, obj.y);
    rotate(obj.rz);
    rect(0, 0, obj.w, obj.h);
    popMatrix();
    fill(52);
    if (output_mode == 1 || output_mode == 2) {
      textAlign(LEFT, TOP);
      textSize(obj.w/10);
      text(label, obj.x-obj.w/2, obj.y+obj.h/2-obj.w/10);
      textAlign(CENTER, CENTER);
      textSize(obj.w/2);
      text(value, obj.x, obj.y);
    }
    if (output_mode == 3) {
      textAlign(CENTER, CENTER);
      textSize(obj.w/10);
      text(label, obj.x, obj.y);
    }
    popStyle();
    popMatrix();
  }
}

void updateAllDataObjects(int output_mode) {
  for (DataObject obj : DOlist) {
    if (obj.multiControl == false) {
      int numOfBlobs = obj.getCtrlCounts();
      if (numOfBlobs<=0) {
        if (obj.bEngaged) { //[Event: Tagged Object Removing From a Data Object]
          obj.val += obj.tempVal;
          obj.tempVal = 0;
          obj.getSTGestureType();
          obj.bEngaged = false;
        }
      } else if (numOfBlobs>0) {
        PVector m = new PVector(0, 0);
        float theta = 0;
        float rx = 0;
        float ry = 0;
        for (TaggedObject b : tm.getActiveTOs()) {
          if (b.getTO_ID() == obj.ctrlIDList.get(0)) {
            m = img2screen(transformPoint(new PVector(b.tx, b.ty, b.tz), homography));
            theta = b.rz-global_rz;
          }
        }
        if (!obj.bEngaged) { //[Event: Tagged Object Landing On a Data Object]
          obj.theta0 = theta-obj.prev_rotation;
          obj.theta_p = obj.theta0;
          obj.m0 = new PVector(m.x, m.y);
          obj.bEngaged = true;
          obj.gestureType = obj.UNDEFINED; //by default
          obj.numTouches = numOfBlobs;
          obj.lastCtrlID = obj.ctrlIDList.get(0);
          obj.gesturePerformed = true;
        } else { //[Event: Tagged Object Updating On a Data Object]
          float newAngle = unwrapAngle(theta, obj.theta_p);
          obj.rotation = -(obj.theta0-newAngle);
          obj.theta_p = newAngle;
          obj.translation = PVector.sub(m, obj.m0);
          if (numOfBlobs>obj.numTouches) obj.numTouches = numOfBlobs;

          switch(output_mode) { //Datxa Behaviors: in "ContinuousGestures" tab
          case 1:
            DO_setValue(obj.dataID, obj.lastCtrlID);
            break;
          case 2:
            DO_setValueLoc2D(obj.dataID, obj.lastCtrlID);
            break;
          case 3:
            DO_setLocOri2D(obj.dataID, obj.lastCtrlID);
            break;
          default:
            break;
          }
        }
      }
    }
  }
}

void drawAllGestures() {
  for (DataObject obj : DOlist) {
    if (obj.multiControl == false) {
      int numOfBlobs = obj.getCtrlCounts();
      if (numOfBlobs==0) {
        obj.drawSTGestureType(); //check this function for the triggers of discrete gestures.
      } else {
        obj.drawSTGestureInfo(); //check this function for the triggers of discrete gestures.
      }
    }
  }
}

float unwrapAngle(float currentAngle, float previousAngle) {
  // Calculate the difference from the previous angle
  float delta = previousAngle - currentAngle;
  
  // Calculate the number of full 2*PI rotations needed to get
  // as close as possible to the previous angle
  int rotations = round(delta / TWO_PI);
  
  // Apply the correct number of rotations to the current angle
  return currentAngle + rotations * TWO_PI;
}

void drawCalibImage() {
  pushStyle();
  imageMode(CENTER);
  image(calibImg, width/2, height/2, (float)calibImg.width*tag2screenRatio, (float)calibImg.height*tag2screenRatio);
  popStyle();
}

void drawCanvas() {
  pushStyle();
  noStroke();
  fill(10);
  rectMode(CENTER);
  rect(width/2, height/2, (float)calibImg.width*tag2screenRatio, (float)calibImg.height*tag2screenRatio);
  popStyle();
}

void showInfo(String s, int x, int y) {
  pushStyle();
  fill(52);
  textAlign(LEFT, BOTTOM);
  textSize(48);
  text(s, x, y);
  popStyle();
}