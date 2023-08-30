const Navbar = () => {
  return (
    <div className="flex justify-between items-center h-16 bg-[#94B8E8] text-[#04387D] px-10 ">
      {/* Logo */}
      <div className="flex items-center">
        <img src="/logoNav.png" alt="Logo" className="w-36 h-36 mr-4" />
      </div>

      {/* Navigasi */}
      <ul className="flex space-x-12 ml-64">
        <li><a href="#" className="hover:text-gray-300">Home</a></li>
        <li><a href="#" className="hover:text-gray-300">List</a></li>
        <li><a href="#" className="hover:text-gray-300">Masjid</a></li>
        <li><a href="#" className="hover:text-gray-300">About</a></li>
      </ul>

      {/* Profil Username */}
      <div className="flex items-center">
        <img src="/profile-picture.svg" alt="Profile" className="w-8 h-8 rounded-full mr-4" />
        <span>Username</span>
      </div>
    </div>
  );
}

export default Navbar;