export default function TestimonialCard({ image, alt, name, children }) {
  return (
    <>
      <div className="flex flex-col items-center justify-center h-screen py-[200px] basic-gradient">
        <div className="max-w-[340px] p-6 rounded-lg bg-white space-y-4 shadow-xl shadow-gray-300/60 border border-gray-100">
          <div className="flex gap-4">
            <img src={image} alt={alt} className="w-12 h-12" />
            <div className="space-y-[1px]">
              <h1 className="text-lg font-semibold text-ellipsis whitespace-nowrap overflow-hidden text-neutral-900 font-['Noto_Sans']">
                {name}
              </h1>
              <p className="text-sm text-zinc-600 text-ellipsis whitespace-nowrap overflow-hidden font-['Noto_Sans']">@saradole</p>
            </div>
          </div>
          <div>
            <p className="text-base text-zinc-600 line-clamp-6 font-['Noto_Sans']">{children}</p>
          </div>
        </div>
      </div>
    </>
  );
}
