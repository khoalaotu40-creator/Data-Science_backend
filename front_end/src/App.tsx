import React, { useState, useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

const steps = [
  {
    title: "Xử lý Văn bản & Parsing",
    desc: "Trong giai đoạn này, các tài liệu pháp lý thô (PDF, Word) được phân tích cú pháp để hiểu cấu trúc phân cấp. Hệ thống không chỉ xem văn bản là một chuỗi ký tự, mà nhận diện rõ ràng đâu là phạm vi điều chỉnh, đối tượng áp dụng và các định nghĩa thuật ngữ quan trọng."
  },
  {
    title: "Trích xuất Thực thể & Quan hệ",
    desc: "Các thuật toán NLP chuyên biệt cho luật pháp sẽ trích xuất 'Thực thể' (ví dụ: Cơ quan thuế, Người nộp thuế) và 'Quan hệ' (ví dụ: Có nghĩa vụ, Được quyền). Những thông tin này tạo thành các node và edge trong Đồ thị Tri thức."
  },
  {
    title: "Truy xuất Đồ thị (Graph Retrieval)",
    desc: "Khi người dùng đặt câu hỏi, hệ thống thực hiện tìm kiếm kép. Nó vừa tìm các đoạn văn bản tương tự về nghĩa, vừa duyệt qua các mối liên kết trên đồ thị để tìm các văn bản hướng dẫn thi hành liên quan trực tiếp đến điều luật đó."
  },
  {
    title: "Tổng hợp & Phản hồi",
    desc: "Cuối cùng, tất cả các dữ liệu đã xác thực được đưa vào LLM. Vì ngữ cảnh được cung cấp từ Đồ thị Tri thức là vô cùng chính xác, câu trả lời tạo ra sẽ có tính chuyên môn cao, đúng thuật ngữ pháp lý và trích dẫn được chính xác điều khoản sử dụng."
  }
];

export default function App() {
  const [activeStep, setActiveStep] = useState(0);
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<any>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number | null>(null);
  const [graphKey, setGraphKey] = useState(0);
  const [isAnimatingStep, setIsAnimatingStep] = useState(false);

  // Initialize Chart.js
  useEffect(() => {
    if (chartRef.current) {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
      const ctx = chartRef.current.getContext('2d');
      if (ctx) {
        chartInstance.current = new Chart(ctx, {
          type: 'radar',
          data: {
            labels: ['Độ chính xác', 'Khả năng trích dẫn', 'Tốc độ phản hồi', 'Logic suy luận', 'Giảm ảo giác', 'Dung lượng dữ liệu'],
            datasets: [
              {
                label: 'RAG Truyền thống',
                data: [65, 40, 85, 50, 60, 90],
                backgroundColor: 'rgba(148, 163, 184, 0.2)',
                borderColor: 'rgba(148, 163, 184, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(148, 163, 184, 1)'
              },
              {
                label: 'LegalGraphRAG',
                data: [92, 98, 75, 95, 90, 85],
                backgroundColor: 'rgba(79, 70, 229, 0.2)',
                borderColor: 'rgba(79, 70, 229, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(79, 70, 229, 1)'
              }
            ]
          },
          options: {
            maintainAspectRatio: false,
            scales: {
              r: {
                beginAtZero: true,
                max: 100,
                ticks: { display: false }
              }
            },
            plugins: {
              legend: { position: 'bottom' }
            }
          }
        });
      }
    }
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, []);

  // Graph Simulation Animation
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const gctx = canvas.getContext('2d');
    if (!gctx) return;

    let nodes: any[] = [];
    let edges: any[] = [];

    const initGraph = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = 400;
      nodes = [];
      edges = [];

      const colors = ['#4f46e5', '#94a3b8', '#cbd5e1'];
      for (let i = 0; i < 15; i++) {
        nodes.push({
          x: Math.random() * (canvas.width - 40) + 20,
          y: Math.random() * (canvas.height - 40) + 20,
          vx: (Math.random() - 0.5) * 1,
          vy: (Math.random() - 0.5) * 1,
          radius: Math.random() * 5 + 5,
          color: colors[Math.floor(Math.random() * colors.length)]
        });
      }

      for (let i = 0; i < 20; i++) {
        edges.push({
          from: Math.floor(Math.random() * nodes.length),
          to: Math.floor(Math.random() * nodes.length)
        });
      }
    };

    const animateGraph = () => {
      gctx.clearRect(0, 0, canvas.width, canvas.height);

      edges.forEach(edge => {
        const n1 = nodes[edge.from];
        const n2 = nodes[edge.to];
        gctx.beginPath();
        gctx.moveTo(n1.x, n1.y);
        gctx.lineTo(n2.x, n2.y);
        gctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        gctx.stroke();
      });

      nodes.forEach(node => {
        node.x += node.vx;
        node.y += node.vy;

        if (node.x < 0 || node.x > canvas.width) node.vx *= -1;
        if (node.y < 0 || node.y > canvas.height) node.vy *= -1;

        gctx.beginPath();
        gctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        gctx.fillStyle = node.color;
        gctx.fill();

        gctx.shadowBlur = 10;
        gctx.shadowColor = node.color;
      });

      animationRef.current = requestAnimationFrame(animateGraph);
    };

    initGraph();
    animateGraph();

    const handleResize = () => {
      canvas.width = canvas.offsetWidth;
    };
    window.addEventListener('resize', handleResize);

    return () => {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      window.removeEventListener('resize', handleResize);
    };
  }, [graphKey]);

  const handleStepChange = (index: number) => {
    setIsAnimatingStep(true);
    setTimeout(() => {
      setActiveStep(index);
      setIsAnimatingStep(false);
    }, 200);
  };

  const resetGraph = () => {
    setGraphKey(prev => prev + 1);
  };

  return (
    <div className="antialiased font-sans bg-slate-50 text-slate-900 min-h-screen flex flex-col">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 h-20 border-b border-slate-200 flex items-center justify-between px-6 lg:px-12 bg-white">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-indigo-600 flex items-center justify-center text-white font-bold" style={{ transform: 'rotate(45deg)' }}>
            <span style={{ transform: 'rotate(-45deg)' }}>L</span>
          </div>
          <span className="font-bold text-xl tracking-tight uppercase">LegalGraph.</span>
        </div>
        <div className="hidden md:flex gap-8 text-sm font-medium uppercase tracking-widest text-slate-500">
          <a href="#tong-quan" className="hover:text-indigo-600 transition-colors">Tổng quan</a>
          <a href="#kien-truc" className="hover:text-indigo-600 transition-colors">Kiến trúc</a>
          <a href="#hieu-nang" className="hover:text-indigo-600 transition-colors">Hiệu năng</a>
          <a href="#mo-phong" className="hover:text-indigo-600 transition-colors">Mô phỏng</a>
        </div>
      </nav>

      <main className="pt-20 flex-1 flex flex-col">
        {/* Hero Section */}
        <section id="tong-quan" className="px-6 lg:px-12 max-w-[1440px] mx-auto w-full pt-16 pb-20">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center mb-16">
            <div className="lg:col-span-8">
              <h1 className="text-5xl md:text-7xl font-black leading-tight tracking-tighter text-slate-900 uppercase">
                Tương Lai <span className="text-indigo-600">Pháp Lý</span><br/> Thông Minh.
              </h1>
              <p className="mt-6 text-lg text-slate-500 max-w-2xl leading-relaxed">
                LegalGraphRAG là sự kết hợp đột phá giữa Đồ thị Tri thức (Knowledge Graph) và Mô hình Ngôn ngữ Lớn (LLM),
                giúp giải quyết các bài toán tra cứu văn bản luật phức tạp với độ chính xác và tính minh bạch tuyệt đối.
              </p>
              <div className="mt-10 flex gap-4">
                <a href="#mo-phong" className="h-12 px-8 bg-indigo-600 flex items-center justify-center text-white font-bold uppercase text-xs tracking-widest hover:bg-indigo-700 transition-colors">Xem Mô Phỏng</a>
                <a href="#kien-truc" className="h-12 w-12 border-2 border-slate-200 flex items-center justify-center text-slate-900 hover:bg-slate-100 transition-colors">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path></svg>
                </a>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 border border-slate-200 bg-white">
            <div className="border-b md:border-b-0 md:border-r border-slate-200 p-10 flex flex-col justify-between hover:bg-slate-50 transition-colors">
              <div>
                <span className="text-xs font-bold text-indigo-600 uppercase tracking-widest">01</span>
                <h3 className="text-xl font-black mt-2 uppercase tracking-tight text-slate-900">Chính xác hơn</h3>
              </div>
              <p className="text-sm text-slate-500 leading-relaxed mt-4">Giảm thiểu hiện tượng "ảo giác" của AI bằng cách neo dữ liệu vào các quan hệ thực thể pháp lý thực tế.</p>
            </div>
            <div className="border-b md:border-b-0 md:border-r border-slate-200 p-10 flex flex-col justify-between hover:bg-slate-50 transition-colors">
              <div>
                <span className="text-xs font-bold text-indigo-600 uppercase tracking-widest">02</span>
                <h3 className="text-xl font-black mt-2 uppercase tracking-tight text-slate-900">Kết nối Đa chiều</h3>
              </div>
              <p className="text-sm text-slate-500 leading-relaxed mt-4">Tự động liên kết các điều luật chéo, nghị định hướng dẫn và các tiền lệ án liên quan.</p>
            </div>
            <div className="p-10 flex flex-col justify-between hover:bg-slate-50 transition-colors">
              <div>
                <span className="text-xs font-bold text-indigo-600 uppercase tracking-widest">03</span>
                <h3 className="text-xl font-black mt-2 uppercase tracking-tight text-slate-900">Trích dẫn Minh bạch</h3>
              </div>
              <p className="text-sm text-slate-500 leading-relaxed mt-4">Mỗi câu trả lời đều đi kèm với nguồn gốc chính xác từ hệ thống đồ thị tri thức.</p>
            </div>
          </div>
        </section>

        {/* Architecture Section */}
        <section id="kien-truc" className="border-t border-slate-200 bg-white">
          <div className="px-6 lg:px-12 max-w-[1440px] mx-auto py-20">
            <div className="mb-12">
              <h2 className="text-4xl font-black text-slate-900 mb-4 uppercase tracking-tighter">Quy trình Hoạt động</h2>
              <p className="text-slate-500 text-lg max-w-2xl">Hệ thống chuyển đổi dữ liệu phi cấu trúc thành mạng lưới tri thức pháp lý có cấu trúc.</p>
            </div>

            <div className="flex flex-col lg:flex-row gap-0 border border-slate-200">
              <div className="w-full lg:w-1/2 flex flex-col border-b lg:border-b-0 lg:border-r border-slate-200">
                {steps.map((step, index) => (
                  <button
                    key={index}
                    onClick={() => handleStepChange(index)}
                    className={`text-left p-8 border-b border-slate-200 transition-colors last:border-b-0 ${
                      activeStep === index ? 'bg-slate-50 border-l-4 border-l-indigo-600' : 'bg-white border-l-4 border-l-transparent hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex flex-col">
                      <span className="text-xs font-bold text-indigo-600 uppercase tracking-widest mb-2">{`0${index + 1}`}</span>
                      <h4 className="font-black text-lg uppercase tracking-tight text-slate-900">{step.title}</h4>
                      <p className="text-sm text-slate-500 mt-2 line-clamp-1">
                        {index === 0 && "Phân tách cấu trúc văn bản luật: Chương, Mục, Điều."}
                        {index === 1 && "Nhận diện các thực thể pháp lý và mối liên hệ giữa chúng."}
                        {index === 2 && "Tìm kiếm thông tin dựa trên cả ngữ nghĩa và cấu trúc đồ thị."}
                        {index === 3 && "LLM tạo câu trả lời dựa trên ngữ cảnh đã được xác thực."}
                      </p>
                    </div>
                  </button>
                ))}
              </div>

              <div className="w-full lg:w-1/2 p-12 bg-slate-50 min-h-[400px] flex flex-col justify-center relative overflow-hidden">
                {/* Decorative background grid pattern */}
                <div className="absolute inset-0 opacity-[0.03] bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
                
                <div className="relative z-10" style={{ opacity: isAnimatingStep ? 0 : 1, transition: 'opacity 0.2s ease-in-out' }}>
                  <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-widest mb-4 block">Chi tiết Bước {`0${activeStep + 1}`}</span>
                  <h3 className="text-3xl font-black text-slate-900 mb-6 uppercase tracking-tighter leading-tight">{steps[activeStep].title}</h3>
                  <p className="text-slate-600 leading-relaxed text-lg">
                    {steps[activeStep].desc}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Performance Section */}
        <section id="hieu-nang" className="border-t border-slate-200 bg-slate-50 py-20 px-6 lg:px-12">
          <div className="max-w-[1440px] mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-widest mb-2 block">Benchmarks</span>
              <h2 className="text-4xl font-black text-slate-900 mb-6 uppercase tracking-tighter leading-tight">Sự Vượt Trội So Với<br/>RAG Truyền Thống</h2>
              <p className="text-slate-600 mb-8 leading-relaxed text-lg">
                Khác với RAG thông thường chỉ dựa trên tìm kiếm vector (semantic similarity), LegalGraphRAG khai thác các mối quan hệ logic. Biểu đồ dưới đây thể hiện kết quả kiểm thử trên bộ dữ liệu luật pháp quốc gia.
              </p>
              <div className="flex flex-col border-t border-slate-200">
                <div className="flex items-start gap-4 border-b border-slate-200 py-4">
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-widest mt-1 w-24">Precision</span>
                  <span className="text-sm text-slate-700 leading-relaxed flex-1">Tăng 35% nhờ khả năng loại bỏ các tài liệu gây nhiễu và lọc theo đồ thị.</span>
                </div>
                <div className="flex items-start gap-4 border-b border-slate-200 py-4">
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-widest mt-1 w-24">Reasoning</span>
                  <span className="text-sm text-slate-700 leading-relaxed flex-1">Xử lý mượt mà các câu hỏi cần tổng hợp thông tin từ 3-5 văn bản khác nhau.</span>
                </div>
                <div className="flex items-start gap-4 py-4">
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-widest mt-1 w-24">Velocity</span>
                  <span className="text-sm text-slate-700 leading-relaxed flex-1">Giảm thiểu tối đa thời gian kiểm tra chéo thủ công cho các chuyên gia luật.</span>
                </div>
              </div>
            </div>
            <div className="bg-white p-8 border border-slate-200 shadow-sm relative">
              <div className="absolute -top-3 -right-3 w-6 h-6 bg-indigo-600"></div>
              <div className="chart-container relative w-full h-[350px]">
                <canvas ref={chartRef}></canvas>
              </div>
              <p className="text-left text-[10px] uppercase tracking-widest font-bold text-slate-400 mt-6 border-t border-slate-100 pt-4">Benchmarking Test 2024 (Thang điểm 100)</p>
            </div>
          </div>
        </section>

        {/* Knowledge Graph Simulation */}
        <section id="mo-phong" className="bg-slate-900 border-t border-slate-800 text-white">
          <div className="px-6 lg:px-12 max-w-[1440px] mx-auto py-20">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              <div className="lg:col-span-4 flex flex-col h-full">
                <div>
                  <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest mb-2 block">Interactive</span>
                  <h2 className="text-4xl font-black mb-6 uppercase tracking-tighter leading-tight">Mô phỏng Đồ thị Tri thức</h2>
                  <p className="text-slate-400 text-sm mb-10 leading-relaxed">
                    Quan sát cách LegalGraphRAG tổ chức dữ liệu. Các nút đại diện cho các thực thể pháp lý, các đường nối thể hiện quan hệ dẫn chiếu hoặc ràng buộc.
                  </p>
                  
                  <div className="space-y-4 mb-10 border-l-2 border-slate-800 pl-6">
                    <div className="flex items-center gap-3">
                      <div className="w-3 h-3 bg-indigo-500"></div>
                      <span className="text-[10px] uppercase tracking-widest font-bold text-slate-300">Văn bản Luật (Gốc)</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="w-3 h-3 bg-slate-400"></div>
                      <span className="text-[10px] uppercase tracking-widest font-bold text-slate-300">Nghị định / Thông tư</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="w-3 h-3 bg-slate-300"></div>
                      <span className="text-[10px] uppercase tracking-widest font-bold text-slate-300">Tiền lệ án</span>
                    </div>
                  </div>
                </div>
                <button onClick={resetGraph} className="mt-auto h-12 w-48 bg-indigo-600 flex items-center justify-center text-white font-bold uppercase text-[10px] tracking-widest hover:bg-indigo-500 transition-colors">
                  Làm mới Đồ thị
                </button>
              </div>
              
              <div className="lg:col-span-8 bg-slate-950 border border-slate-800 p-2 relative">
                {/* Four corner accents */}
                <div className="absolute top-0 left-0 w-2 h-2 border-t border-l border-slate-500"></div>
                <div className="absolute top-0 right-0 w-2 h-2 border-t border-r border-slate-500"></div>
                <div className="absolute bottom-0 left-0 w-2 h-2 border-b border-l border-slate-500"></div>
                <div className="absolute bottom-0 right-0 w-2 h-2 border-b border-r border-slate-500"></div>
                
                <canvas ref={canvasRef} className="w-full h-[400px] bg-slate-900"></canvas>
              </div>
            </div>
          </div>
        </section>

        {/* Summary Section */}
        <section className="bg-white border-t border-slate-200">
          <div className="max-w-[1440px] mx-auto px-6 lg:px-12 py-20">
            <div className="text-center mb-12">
              <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-widest mb-2 block">Impact</span>
              <h2 className="text-4xl font-black text-slate-900 mb-4 uppercase tracking-tighter">Tác động Chiến lược</h2>
              <p className="text-slate-500 text-lg max-w-2xl mx-auto">
                Triển khai LegalGraphRAG để tái định nghĩa cách các tổ chức pháp lý quản trị tri thức.
              </p>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 border border-slate-200 max-w-4xl mx-auto">
              <div className="p-12 bg-white border-b sm:border-b-0 sm:border-r border-slate-200 flex flex-col hover:bg-slate-50 transition-colors">
                <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-widest mb-4">Enterprise</span>
                <h4 className="font-black text-2xl text-slate-900 mb-4 uppercase tracking-tighter">Doanh nghiệp</h4>
                <p className="text-sm text-slate-600 leading-relaxed">Tự động hóa rà soát hợp đồng, tuân thủ pháp luật và giảm chi phí thuê chuyên gia bên ngoài cho các tác vụ tra cứu cơ bản.</p>
              </div>
              <div className="p-12 bg-white flex flex-col hover:bg-slate-50 transition-colors">
                <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-widest mb-4">Government</span>
                <h4 className="font-black text-2xl text-slate-900 mb-4 uppercase tracking-tighter">Nhà làm luật</h4>
                <p className="text-sm text-slate-600 leading-relaxed">Phát hiện mâu thuẫn giữa các văn bản luật mới và cũ, đảm bảo tính thống nhất trong hệ thống pháp luật quốc gia.</p>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="h-20 bg-slate-900 text-white flex items-center justify-between px-6 lg:px-12">
        <p className="text-[10px] uppercase tracking-widest font-medium opacity-60">
          © 2024 LegalGraphRAG / All Rights Reserved
        </p>
        <div className="hidden md:flex gap-8 text-[10px] uppercase tracking-widest font-bold">
          <span className="opacity-100 hover:text-indigo-400 cursor-pointer transition-colors">Báo cáo đầy đủ</span>
          <span className="opacity-40 hover:opacity-100 cursor-pointer transition-colors">Tài liệu API</span>
          <span className="opacity-40 hover:opacity-100 cursor-pointer transition-colors">Liên hệ</span>
        </div>
        <p className="text-[10px] uppercase tracking-widest font-medium opacity-60">
          Built with Precision
        </p>
      </footer>
    </div>
  );
}
