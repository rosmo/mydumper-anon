class MydumperAnon < Formula
  desc "mydumper-anon is a fork of mydumper with option of data anonymization"
  homepage "https://github.com/rosmo/mydumper-anon"
  url "https://github.com/rosmo/mydumper-anon/archive/v0.9.1.tar.gz"
  sha256 "30589d82d66ed19e1a4f8ca2217b52363ec2c96c157031c21d893bc066c82b34"
  head "https://github.com/rosmo/mydumper-anon.git"

  conflicts_with "mydumper", :because => "both install `mydumper` and `myloader` binaries"

  depends_on "cmake" => :build
  depends_on "pkg-config" => :build
  depends_on "libyaml" => :build
  depends_on "pcre" => :build
  depends_on "mysql"
  depends_on "glib"
  depends_on "gettext"
  depends_on "zlib"

  def install
    # ENV.deparallelize  # if your formula fails when building in parallel
    ENV.append "LDFLAGS", `pkg-config --libs mysqlclient`.chomp
    ENV.append "LDFLAGS", `pkg-config --libs glib-2.0`.chomp
    ENV.append "LDFLAGS", `pkg-config --libs zlib`.chomp

    mysql_pkglibdir  = `mysql_config --variable=pkglibdir`.chomp
    mysql_pkgincludedir = `mysql_config --variable=pkgincludedir`.chomp

    system "cmake", ".",
      "-DMYSQL_LIBRARIES=#{mysql_pkglibdir}",
      "-DMYSQL_INCLUDE_DIR=#{mysql_pkgincludedir}",
      "-DGLIB2_INCLUDE_DIR=#{HOMEBREW_PREFIX}/opt/glib/include/glib-2.0",
      "-DZLIB_LIBRARY=#{HOMEBREW_PREFIX}/opt/zlib/include",
      *std_cmake_args
    system "make", "VERBOSE=1",
      "CC=#{ENV.cc}",
      "CFLAGS=#{ENV.cflags}",
      "LDFLAGS=#{ENV.ldflags}"
    system "make", "install"
  end

  test do
    system bin/"mydumper", "--help"
      system bin/"myloader", "--help"
  end
end
