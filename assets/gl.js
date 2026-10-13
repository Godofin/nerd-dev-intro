// Fundo do hero: shader WebGL com ruído fluido nas cores da marca (azul-petróleo, roxo, magenta).
// Sem WebGL ou com "reduzir movimento", mostra um quadro estático ou o gradiente CSS de reserva.
(() => {
  const canvas = document.querySelector(".hero__gl");
  if (!canvas) return;
  const gl = canvas.getContext("webgl", { antialias: false, alpha: false, powerPreference: "low-power" });
  if (!gl) return;

  const vs = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
  const fs = `
    precision mediump float;
    uniform vec2 r; uniform float t; uniform vec2 m;
    float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
    float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
      return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
    float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<4;i++){v+=a*n(p);p*=2.02;a*=.5;}return v;}
    void main(){
      vec2 uv=gl_FragCoord.xy/r; vec2 p=uv*vec2(r.x/r.y,1.)*1.6;
      vec2 mo=(m-.5)*.35;
      float a=fbm(p+vec2(t*.05,t*.03)+mo);
      float b=fbm(p*1.3+a*1.8+vec2(-t*.04,t*.06));
      vec3 teal=vec3(0.,.569,.678), purple=vec3(.361,.302,.490), mag=vec3(.718,.035,.298), ink=vec3(.055,.043,.086);
      vec3 c=mix(ink,teal,smoothstep(.25,.75,b));
      c=mix(c,purple,smoothstep(.35,.85,a)*.85);
      c=mix(c,mag,smoothstep(.55,.95,a*b*2.1+uv.x*.35)*.9);
      c=mix(ink,c,.62+.38*uv.x);
      gl_FragColor=vec4(c,1.);
    }`;

  const mk = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; };
  const prog = gl.createProgram();
  gl.attachShader(prog, mk(gl.VERTEX_SHADER, vs));
  gl.attachShader(prog, mk(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
  gl.useProgram(prog);

  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, "p");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

  const u = { r: gl.getUniformLocation(prog, "r"), t: gl.getUniformLocation(prog, "t"), m: gl.getUniformLocation(prog, "m") };
  const mouse = { x: .5, y: .5, tx: .5, ty: .5 };
  const reduce = matchMedia("(prefers-reduced-motion: reduce)");
  let running = false, visible = true, start = performance.now();

  function resize() {
    const dpr = Math.min(devicePixelRatio || 1, 1.5);
    const w = Math.max(1, Math.round(canvas.clientWidth * dpr));
    const h = Math.max(1, Math.round(canvas.clientHeight * dpr));
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
    gl.viewport(0, 0, w, h);
  }

  function draw(now) {
    resize();
    mouse.x += (mouse.tx - mouse.x) * .05;
    mouse.y += (mouse.ty - mouse.y) * .05;
    gl.uniform2f(u.r, canvas.width, canvas.height);
    gl.uniform1f(u.t, reduce.matches ? 4 : (now - start) / 1000);
    gl.uniform2f(u.m, mouse.x, 1 - mouse.y);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }

  function loop(now) {
    if (!running) return;
    draw(now);
    requestAnimationFrame(loop);
  }

  function play() {
    if (running || reduce.matches || !visible || document.hidden) return;
    running = true;
    requestAnimationFrame(loop);
  }

  draw(performance.now());
  canvas.classList.add("on");
  if (reduce.matches) return;

  addEventListener("pointermove", (e) => { mouse.tx = e.clientX / innerWidth; mouse.ty = e.clientY / innerHeight; }, { passive: true });
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; running = false; play(); }).observe(canvas);
  document.addEventListener("visibilitychange", () => { running = false; play(); });
  addEventListener("resize", () => draw(performance.now()));
  play();
})();
